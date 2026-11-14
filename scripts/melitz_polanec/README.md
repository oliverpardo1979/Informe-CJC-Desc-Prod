# Productividad empresarial: repositorio activo

Desde el 13 de noviembre de 2026, este repositorio es el destino de todo desarrollo de Melitz–Polanec. La carpeta original de CJC-Monitor se conserva como respaldo, no como copia activa.

## Estructura

- `melitz-polanec.tex`: segundo boletín, reutiliza `Paper/configuracion.tex` y la portada institucional.
- `main.tex`: informe agregado original; permanece independiente.
- `Paper/sections/melitz_polanec/`: texto y cuadro del boletín empresarial.
- `Paper/figures/melitz_polanec/`: figuras de EAM, EAC y EAS.
- `scripts/melitz_polanec/`: scripts 01–09 migrados y adaptados.
- `data/melitz_polanec/`: deflactores y paneles locales; `tables/` contiene resultados agregados versionables.
- `Paper/notes/melitz_polanec/`: notas históricas de decisiones y diagnóstico.

## Reproducción

Ejecutar desde la raíz. Python requiere pandas, matplotlib y openpyxl para figuras y deflactores. R requiere dplyr, readxl y haven. `cuadro_boletin.py` solo utiliza la biblioteca estándar de Python.

Los insumos originales se resuelven mediante `CJC_SOURCE_ROOT`, que apunta a la raíz de CJC-Monitor con su carpeta `Datos/`. Por defecto se usa el padre de este checkout, apropiado para la instalación actual. En otro equipo se debe configurar explícitamente, por ejemplo en PowerShell:

```powershell
$env:CJC_SOURCE_ROOT = 'C:/ruta/CJC-Monitor'
Rscript scripts/melitz_polanec/01_diagnostico_EAM.R
Rscript scripts/melitz_polanec/02_deflactor_IPP.R
Rscript scripts/melitz_polanec/03_panel_empresas_EAM.R
Rscript scripts/melitz_polanec/04_DOPD_productividad_laboral.R
python scripts/melitz_polanec/05_figura_DOPD_laboral.py
python scripts/melitz_polanec/06_deflactores_comercio_servicios.py
Rscript scripts/melitz_polanec/07_panel_empresas_EAC_EAS.R
Rscript scripts/melitz_polanec/08_DOPD_comercio_servicios.R
python scripts/melitz_polanec/09_figura_DOPD_comercio_servicios.py
python scripts/melitz_polanec/cuadro_boletin.py
pdflatex -interaction=nonstopmode -halt-on-error melitz-polanec.tex
pdflatex -interaction=nonstopmode -halt-on-error melitz-polanec.tex
```

Para compilar desde resultados existentes basta ejecutar las últimas tres líneas. En Overleaf seleccionar `melitz-polanec.tex` como documento principal para este boletín; `main.tex` sigue compilando el informe original.

## Estado y límites

Industria, comercio y servicios implementados; comparación DOPD/GR/FHK disponible. Robustez y PTF empresarial pendientes. No interpretar el índice de logaritmos como el cociente agregado VA/empleo. La reasignación es el cambio de una covarianza y no identifica flujos de trabajadores. Entrada y salida son de la muestra.

Las notas 01–03 conservan estados históricos; la extensión a EAC/EAS está documentada en la nota 04. Las rutas relativas de esas notas son las originales de archivo; esta guía y los scripts contienen las rutas operativas actuales.

No versionar microdatos ni paneles empresariales: `.rds`, `.dta`, `.sav` y `.pkl` están excluidos. No se incorporó el PDF del artículo; la referencia bibliográfica está en el boletín.
