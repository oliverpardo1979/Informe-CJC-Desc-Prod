"""Reproduce los resultados del anexo de productividad laboral del DANE."""
from __future__ import annotations

import csv
import hashlib
import math
import re
import sys
from pathlib import Path
from statistics import mean

from openpyxl import load_workbook
from reportlab.lib.colors import HexColor
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ROOT / "Paper" / "sections"
FIGURES = ROOT / "Paper" / "figures"
YEARS = list(range(2005, 2026))


def load_sheet(sheet, cols):
    results = {}
    for row in sheet.iter_rows(min_row=15, max_row=35, values_only=True):
        year = int(re.fullmatch(r"(20\d\d)(?:p|pr)?", str(row[1])).group(1))
        assert year not in results
        results[year] = [float(row[i]) for i in cols]
    assert list(results) == YEARS
    return results


def check(hour, person):
    implied_share_exceptions = []
    for year in YEARS:
        h, n = hour[year], person[year]
        assert math.isclose(h[0], sum(h[1:]), abs_tol=1e-10)
        assert math.isclose(n[0], sum(n[1:]), abs_tol=1e-10)
        assert n[1:3] == h[1:3], year
        gap = n[0] - h[0]
        assert math.isclose(gap, n[4] + n[3] - h[3], abs_tol=1e-10)
        # El aporte directo de horas es la variación por persona ponderada.
        if not 0 < n[4] / gap < 1:
            implied_share_exceptions.append(year)
    assert implied_share_exceptions == [2010, 2015], implied_share_exceptions
    # Cotejo de las cuatro cifras citadas en el resumen y en la sección 4.
    assert round(mean(x[0] for x in hour.values()), 2) == 1.03
    assert round(mean(x[0] for x in person.values()), 2) == 0.88
    assert round(mean(hour[y][0] for y in range(2022, 2026)), 2) == 0.31
    assert round(mean(person[y][0] for y in range(2022, 2026)), 2) == -1.17


def fmt(value):
    return rf"\({value:.2f}\)".replace(".", "{,}")


def write_tex(filename, rows):
    (SECTIONS / filename).write_text("\n".join(rows) + "\n", encoding="utf-8")


def tables(hour, person):
    h, n = hour[2025], person[2025]
    rows = [
        r"\begin{tabularx}{\linewidth}{@{}Xrr@{}}",
        r"\toprule",
        r" & \textbf{Por hora} & \textbf{Por persona} \\",
        r"\midrule",
        f"Productividad laboral (\\%) & {fmt(h[0])} & {fmt(n[0])} \\\\",
        r"\addlinespace",
        r"\multicolumn{3}{@{}l}{Aportes al crecimiento (pp)} \\",
    ]
    for label, i in [("Productividad total de los factores", 1),
                     ("Composición del trabajo", 2),
                     ("Servicios de capital por hora o persona", 3),
                     ("Horas trabajadas por persona (aporte directo)", 4)]:
        rows.append(f"{label} & {fmt(h[i]) if i < 4 else '---'} & {fmt(n[i])} \\\\")
    write_tex("Cuadro2025.tex", rows + [r"\bottomrule", r"\end{tabularx}"])

    rows = [
        r"\small",
        r"\begin{tabularx}{\linewidth}{@{}Xrrrrr@{}}",
        r"\toprule",
        r"Periodo & Total & PTF & Composición & Capital & Horas \\",
    ]
    for label, values in [("Por hora trabajada", hour), ("Por persona empleada", person)]:
        rows.extend([r"\midrule", rf"\multicolumn{{6}}{{@{{}}l}}{{\textbf{{{label}}}}} \\"])
        for a, b in [(2005, 2019), (2020, 2021), (2022, 2025), (2005, 2025)]:
            sample = [values[y] for y in range(a, b + 1)]
            means = [fmt(mean(c)) for c in zip(*sample)]
            if values is hour:
                means.append("---")
            rows.append(f"{a}--{b} & " + " & ".join(means) + r" \\")
    write_tex("CuadroPeriodos.tex", rows + [r"\bottomrule", r"\end{tabularx}"])


def figure(hour, person):
    palette = ("#005B83", "#8C452E")
    graph = Canvas(str(FIGURES / "series.pdf"), pagesize=(450, 205), invariant=1)
    graph.setTitle("Productividad laboral por hora y por persona en Colombia")
    left, right, bottom, top = 36, 375, 30, 168
    xp = lambda year: left + (year - 2004) * (right - left) / 21
    yp = lambda val: bottom + (val - 99) * (top - bottom) / 29
    graph.setFillColor(HexColor("#263642"))
    graph.setFont("Helvetica", 10)
    graph.drawString(left, 188, "Índice (2004 = 100)")
    for value in (100, 105, 110, 115, 120, 125):
        y = yp(value)
        graph.setStrokeColor(HexColor("#D5DEE3"))
        graph.setLineWidth(0.65)
        graph.line(left, y, right, y)
        graph.drawRightString(left - 7, y - 3, str(value))
    for year in (2004, 2009, 2014, 2019, 2025):
        graph.drawCentredString(xp(year), bottom - 14, str(year))
    for data, title, color, dash in (
        (hour, "Por hora", palette[0], []),
        (person, "Por persona", palette[1], [4, 2]),
    ):
        series = [(xp(2004), yp(100))]
        acc = 0
        for year in YEARS:
            acc += data[year][0] / 100
            series.append((xp(year), yp(100 * math.exp(acc))))
        graph.setStrokeColor(HexColor(color))
        graph.setFillColor(HexColor(color))
        graph.setLineWidth(1.85)
        graph.setDash(dash)
        path = graph.beginPath()
        path.moveTo(*series[0])
        for x, y in series[1:]:
            path.lineTo(x, y)
        graph.drawPath(path)
        graph.setDash([])
        x, y = series[-1]
        graph.circle(x, y, 2, fill=1, stroke=0)
        graph.setFont("Helvetica-Bold", 10)
        graph.drawString(x + 7, y - 3, title)
    graph.showPage()
    graph.save()


def main(source):
    book = load_workbook(source, read_only=True, data_only=True)
    hour = load_sheet(book["Cuadro 1"], (2, 3, 4, 5))
    # La columna G reproduce la composición del Cuadro 1 en todos los años.
    person = load_sheet(book["Cuadro 2"], (2, 3, 6, 5, 4))
    check(hour, person)
    sha = hashlib.sha256(source.read_bytes()).hexdigest()
    with (ROOT / "data" / "productividad_laboral.csv").open(
        "w", encoding="utf-8", newline=""
    ) as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow([
            "anio", "estado", "productividad_hora_pct_log", "productividad_persona_pct_log",
            "ptf_pp", "composicion_pp", "capital_por_hora_pp", "capital_por_persona_pp",
            "aporte_directo_horas_por_persona_pp", "horas_por_persona_pct_log",
        ])
        for year in YEARS:
            h, n = hour[year], person[year]
            status = {2024: "provisional", 2025: "preliminar"}.get(year, "")
            writer.writerow([year, status, h[0], n[0], *h[1:], n[3], n[4], n[0] - h[0]])
    (ROOT / "data" / "fuente.txt").write_text(
        "https://www.dane.gov.co/files/operaciones/PTF/anex-PTF-ProductividadLaboral-2025.xlsx\n"
        f"SHA-256: {sha}\n"
        "Cuadro 1 y Cuadro 2, filas 15 a 35. En Cuadro 2, F = capital, G = composición.\n",
        encoding="utf-8",
    )
    tables(hour, person)
    figure(hour, person)
    print(f"Identidades comprobadas en {len(YEARS)} años. SHA-256: {sha}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
