# Migración y validación — 13 de noviembre de 2026

El desarrollo continúa en Informe-CJC-Desc-Prod. Se conservaron los archivos del informe agregado original y se agregó una entrada independiente `melitz-polanec.tex`, con ocho páginas y tres figuras.

Validación ejecutada en el nuevo checkout:
- R 4.5.1: scripts 04 y 08 ejecutados sobre los paneles locales migrados. Pasaron las identidades DOPD/GR/FHK y los ejemplos sintéticos. Resultados coincidentes con las tablas previas.
- Python: scripts 05 y 09 regeneraron las tres figuras en `Paper/figures/melitz_polanec/`.
- `cuadro_boletin.py`: verificó el cierre de 12 ventanas y generó ocho filas para el boletín.
- Dos compilaciones pdflatex exitosas; sin referencias indefinidas ni advertencias de cajas desbordadas. Revisión visual del PDF.
- `git diff --check` sin errores; paneles `.rds` ignorados por Git.

Los scripts 01, 02, 03, 06 y 07 tienen rutas adaptadas, pero no se reconstruyeron los paneles desde las fuentes originales durante esta migración. No se ejecutaron nuevas pruebas de robustez.

En este equipo R requirió definir `R_LIBS_USER=C:/Users/jorge/AppData/Local/R/win-library/4.5` para localizar dplyr. Las advertencias de locale de inicio no impidieron la ejecución. En otro equipo deben instalarse las dependencias en su biblioteca propia.

Las notas 01–04 se conservan como historial. Sus menciones a etapas pendientes y rutas deben contrastarse con la guía vigente en `scripts/melitz_polanec/README.md`.
