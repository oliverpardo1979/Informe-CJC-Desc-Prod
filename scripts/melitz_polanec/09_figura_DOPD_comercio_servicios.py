"""Figuras: descomposicion dinamica de Olley-Pakes de la productividad laboral con la EAC (comercio) y la EAS (servicios). Mismo formato que 05_figura_DOPD_laboral.py (EAM).

A. Componentes de la DOPD por ventana.   B. Contribucion de la entrada segun el metodo (DOPD frente a GR y FHK).
Las ventanas no comparables (cambio de cobertura o de identificador) se muestran claras y rayadas, con asterisco.
Entradas: Outputs/tables/dopd_laboral_ventanas_comercio_servicios.csv y dopd_laboral_comparacion_comercio_servicios.csv
Salidas : Outputs/Figures/fig_dopd_laboral_EAC.png y fig_dopd_laboral_EAS.png
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[2]
for f in ("segoeui.ttf", "segoeuib.ttf"):
    p = Path(r"C:\Windows\Fonts") / f
    if p.exists():
        font_manager.fontManager.addfont(str(p))
plt.rcParams["font.family"] = ["Segoe UI", "DejaVu Sans"]
INK, INK2, MUTED, GRID, AXIS = "#14202B", "#46535F", "#7A8791", "#E7EBEE", "#C9D1D6"
COL = {"dentro_media_sobrevivientes": "#9AA7B0", "reasignacion_covarianza_sobrevivientes": "#2A78D6", "entrada": "#EB6834", "salida": "#1BAF7A"}
LAB = {"dentro_media_sobrevivientes": "Mejora dentro de las empresas (media sin ponderar)", "reasignacion_covarianza_sobrevivientes": "Reasignación entre sobrevivientes (covarianza)",
       "entrada": "Entrada", "salida": "Salida"}
T = ROOT / "data" / "melitz_polanec" / "tables"
res_all = pd.read_csv(T / "dopd_laboral_ventanas_comercio_servicios.csv")
cmp_all = pd.read_csv(T / "dopd_laboral_comparacion_comercio_servicios.csv")
c1 = lambda x: f"{x:.1f}".replace(".", ",")

CONFIG = {
    "EAC": dict(titulo="Productividad laboral del comercio colombiano: de dónde viene el cambio", orden=["2010-2015", "2015-2019", "2020-2024"],
                sub="Descomposición dinámica de Olley–Pakes (Melitz y Polanec, 2015). EAC, empresas de comercio, valor agregado real por trabajador y participaciones de empleo.",
                nota=("Fuente: DANE (EAC; PIB departamental, deflactor implícito de comercio, transporte y alojamiento) y cálculos propios. La EAC cambia de identificador de empresa en 2020: no se puede seguir a las empresas de 2019 a 2024.\n"
                      "* 2010→2015 no es comparable: el universo de la EAC se amplía en 2014 (de ~7.000 a ~10.600 empresas) y antes de 2013 mezcla estratos muestrales; las entradas no son nacimientos. 2020 es un año de pandemia.")),
    "EAS": dict(titulo="Productividad laboral de los servicios colombianos: de dónde viene el cambio", orden=["2010-2015", "2015-2019", "2019-2024"],
                sub="Descomposición dinámica de Olley–Pakes (Melitz y Polanec, 2015). EAS, empresas de servicios, valor agregado real por trabajador y participaciones de empleo.",
                nota=("Fuente: DANE (EAS; PIB departamental, deflactor implícito de servicios) y cálculos propios. La EAS cubre empresas por encima de un umbral de tamaño o ingresos: la entrada y la salida\n"
                      "incluyen empresas que cruzan ese umbral, no solo nacimientos y cierres.")),
}


def figura(enc):
    cfg = CONFIG[enc]
    res = res_all[res_all.encuesta == enc]
    cmp_ = cmp_all[cmp_all.encuesta == enc].set_index("ventana")
    orden = cfg["orden"]
    comp = res.drop_duplicates("ventana").set_index("ventana").comparable.to_dict()
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.9), dpi=200, facecolor="white", gridspec_kw={"width_ratios": [1.15, 1], "wspace": 0.25})
    for a in (ax, ax2):
        a.grid(axis="y", color=GRID, zorder=0)
        a.set_axisbelow(True)
        for sp in ("top", "right"):
            a.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            a.spines[sp].set_color(AXIS)
        a.tick_params(length=0, labelsize=10.5, labelcolor=MUTED)
    lo, hi = 0.0, 0.0
    for i, v in enumerate(orden):
        d = res[res.ventana == v].set_index("componente")
        ok = bool(comp[v])
        pos = neg = 0.0
        for c in COL:
            x = d.loc[c, "valor_pp"]
            kw = dict(color=COL[c], edgecolor="white", linewidth=0.8, zorder=3, alpha=1 if ok else 0.45, hatch=None if ok else "///")
            if x >= 0:
                ax.bar(i, x, 0.55, bottom=pos, **kw)
                pos += x
            else:
                ax.bar(i, x, 0.55, bottom=neg, **kw)
                neg += x
        lo, hi = min(lo, neg), max(hi, pos)
        tot = d["cambio_total"].iloc[0]
        ax.scatter([i], [tot], marker="_", s=420, color=INK, linewidths=2.4, zorder=5)
        ax.text(i + 0.31, tot, c1(tot), va="center", fontsize=10.5, color=INK, fontweight="bold")
        lo, hi = min(lo, tot), max(hi, tot)
    ax.axhline(0, color=AXIS, lw=1.2, zorder=2)
    ax.set_xticks(range(len(orden)))
    ax.set_xticklabels([o.replace("-", " → ") + ("" if comp[o] else "*") for o in orden], fontsize=11, color=INK2)
    ax.set_ylabel("Cambio de la productividad laboral (puntos log × 100)", fontsize=10.5, color=INK2)
    ax.set_title("A. Descomposición del cambio agregado", loc="left", fontsize=12, fontweight="bold", color=INK, pad=10)
    handles = [Patch(color=COL[c], label=LAB[c]) for c in COL] + [plt.Line2D([0], [0], marker="_", color=INK, lw=0, markersize=12, markeredgewidth=2.4, label="Cambio total")]
    ax.legend(handles=handles, loc="upper left", frameon=False, fontsize=9, labelcolor=INK2)
    margen = 0.08 * (hi - lo)
    ax.set_ylim(lo - margen, hi + 0.62 * (hi - lo))

    w = 0.25
    vals = []
    for j, (met, col) in enumerate((("DOPD", "#2A78D6"), ("GR", "#9AA7B0"), ("FHK", "#C9D1D6"))):
        y = cmp_.loc[orden, f"{met}_entrada"].values
        vals += list(y)
        ax2.bar(np.arange(len(orden)) + (j - 1) * w, y, w * 0.92, color=col, edgecolor="white", zorder=3, label=met)
    ax2.axhline(0, color=AXIS, lw=1.2, zorder=2)
    ax2.set_xticks(range(len(orden)))
    ax2.set_xticklabels([o.replace("-", " → ") + ("" if comp[o] else "*") for o in orden], fontsize=11, color=INK2)
    ax2.set_ylabel("Contribución de la entrada (puntos log × 100)", fontsize=10.5, color=INK2)
    ax2.set_title("B. La entrada según el método", loc="left", fontsize=12, fontweight="bold", color=INK, pad=10)
    ax2.legend(loc="upper right" if min(vals) < 0 and max(vals) <= 0.5 else "lower right", frameon=False, fontsize=10, labelcolor=INK2)
    ax2.set_ylim(min(vals) * 1.15 - 0.2, max(max(vals), 0) * 1.25 + 0.3)

    fig.text(0.04, 0.975, cfg["titulo"], fontsize=16, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.925, cfg["sub"], fontsize=10.5, color=INK2, va="top")
    fig.text(0.04, 0.012, cfg["nota"], fontsize=8.3, color=MUTED, va="bottom", linespacing=1.45)
    fig.subplots_adjust(top=0.82, bottom=0.17, left=0.07, right=0.98)
    out = ROOT / "Paper" / "figures" / "melitz_polanec"
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"fig_dopd_laboral_{enc}.png", dpi=200, facecolor="white")
    print("ok", out / f"fig_dopd_laboral_{enc}.png")


for enc in CONFIG:
    figura(enc)
