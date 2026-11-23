# Descomposición de la productividad laboral en Colombia

## Fase actual: revisión de literatura

El documento activo sigue siendo `melitz-polanec.tex` y su salida `melitz-polanec.pdf`. Por decisión editorial, contiene solamente portada, revisión de literatura y referencias. Las secciones de resultados, metodología propia y conclusiones no se incluyen en esta fase. Sus fuentes se conservan para retomarlas después.

La revisión contiene veinte referencias organizadas en cuadros: fundamentos del método, América Latina, otros países y comparabilidad. [Literatura/README.md](Literatura/README.md) y las fichas registran el alcance de cada consulta. Las copias PDF locales se excluyen de Git.

Compilar dos veces con `pdflatex -interaction=nonstopmode -halt-on-error melitz-polanec.tex`. El antiguo integrador `11_actualizar_borrador.py` está desactivado para no reinsertar las secciones retiradas. `main.tex` mantiene independiente el informe agregado original.

Véase [la guía de reproducción de resultados](scripts/melitz_polanec/README.md). Los microdatos no se incorporan al repositorio.
