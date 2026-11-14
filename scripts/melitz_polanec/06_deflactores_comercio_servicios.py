"""Deflactores de valor agregado para comercio (EAC) y servicios (EAS): deflactor implicito = valor agregado a precios corrientes / valor agregado a precios constantes (base 2015).

Fuente: DANE, PIB departamental 2005-2024pr (Datos/Raw/PIB_DANE/anex-PIBDep-departamento-2024pr.xlsx): cuadro 1 (corrientes) y cuadro 2 (series encadenadas de volumen,
año de referencia 2015) por departamento y agrupacion de actividad. Se suman los 33 departamentos de cada grupo (el total nacional por actividad).
La suma de series encadenadas no es exacta lejos del año base; como el deflactor es comun a todas las empresas de cada encuesta, solo desplaza el componente "dentro de las
empresas" de la descomposicion (ver Docs/03_Etapas_1-3_Productividad_laboral.md), asi que esa aproximacion no cambia los componentes de reasignacion, entrada y salida.

Grupos: comercio (EAC) = "G + H + I" (comercio, transporte y alojamiento y comidas); servicios (EAS) = "J" + "M + N" + "O + P + Q" + "R + S + T"
(informacion y comunicaciones, profesionales y apoyo, administracion publica, educacion y salud, artisticas y otros servicios).

Salida: data/melitz_polanec/deflactores_comercio_servicios_anual.csv (anio, defl_comercio, defl_servicios, defl_total; 2015 = 1)
Uso   : python scripts/melitz_polanec/06_deflactores_comercio_servicios.py   (desde la raiz del repositorio)
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
import os
SOURCE = Path(os.environ.get("CJC_SOURCE_ROOT", str(ROOT.parent)))
F = SOURCE / "Datos" / "Raw" / "PIB_DANE" / "anex-PIBDep-departamento-2024pr.xlsx"
GRUPOS = {"comercio": ["G + H + I"], "servicios": ["J", "M + N", "O + P + Q", "R + S + T"],
          "total": ["A", "B", "C", "D + E", "F", "G + H + I", "J", "K", "L", "M + N", "O + P + Q", "R + S + T"]}


def sumar(hoja):
    d = pd.read_excel(F, sheet_name=hoja, header=None)
    anios = []
    for v in d.iloc[9, 3:]:                      # el encabezado repite otras tablas a la derecha: se toma solo el bloque contiguo de años
        t_ = str(v)[:4]
        if pd.isna(v) or not t_.isdigit():
            break
        anios.append(int(t_))
    tit = d.index[d[0].astype(str).str.contains("valor agregado según", case=False, na=False)].tolist()
    acum = {g: np.zeros(len(anios)) for g in GRUPOS}
    for t in tit:
        bloque = d.iloc[t + 6:t + 18]
        for g, codigos in GRUPOS.items():
            sel = bloque[bloque[1].astype(str).str.strip().isin(codigos)]
            acum[g] += sel.iloc[:, 3:3 + len(anios)].apply(pd.to_numeric, errors="coerce").sum().values
    return anios, acum, len(tit)


anios, cor, n1 = sumar("Cuadro 1")
_, con, n2 = sumar("Cuadro 2")
assert n1 == n2 == 33, (n1, n2)
out = pd.DataFrame({"anio": anios})
for g in GRUPOS:
    out[f"defl_{g}"] = cor[g] / con[g]
    out[f"va_corriente_{g}_miles_millones"] = cor[g]
out = out[out.anio >= 2005]
print(out[["anio", "defl_comercio", "defl_servicios", "defl_total"]].round(3).to_string(index=False))
# el deflactor en 2015 debe ser 1 (año de referencia)
assert all(abs(out.loc[out.anio == 2015, f"defl_{g}"].iloc[0] - 1) < 0.02 for g in GRUPOS)
(ROOT / "data" / "melitz_polanec").mkdir(parents=True, exist_ok=True)
out[["anio", "defl_comercio", "defl_servicios", "defl_total"]].to_csv(ROOT / "data" / "melitz_polanec" / "deflactores_comercio_servicios_anual.csv", index=False)
