# Convenciones del proyecto

Este es el repositorio activo para el análisis Melitz–Polanec del CJC.
Mantener el informe agregado existente (`main.tex`) y el empresarial (`melitz-polanec.tex`) como entradas independientes.
Respetar `scripts/`, `data/`, `Paper/sections/` y `Paper/figures/`; usar subcarpetas `melitz_polanec`.
Conservar el formato institucional de `Paper/configuracion.tex`; hacer cambios específicos mediante redefiniciones en la entrada empresarial.
Los insumos externos se localizan con `CJC_SOURCE_ROOT`. Nunca incorporar paneles empresariales o microdatos a Git.
Generar el cuadro con `python scripts/melitz_polanec/cuadro_boletin.py`; compilar dos veces y revisar el PDF antes de entregar cambios de redacción o diseño.
No confundir promedio ponderado de logaritmos con logaritmo de productividad agregada, ni salida de encuesta con cierre de empresa.
No afirmar que las pruebas de robustez están completas hasta ejecutarlas y documentarlas.
