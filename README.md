# Descomposición de la productividad laboral en Colombia

## Boletín empresarial Melitz–Polanec

El análisis de industria, comercio y servicios se desarrolla en este repositorio desde el 13 de noviembre de 2026. Su documento principal es **`melitz-polanec.tex`**, con PDF `melitz-polanec.pdf`. Reutiliza el formato institucional y mantiene independiente el informe agregado de `main.tex`.

Véase [la guía de estructura y reproducción](scripts/melitz_polanec/README.md). Código en `scripts/melitz_polanec/`, resultados en `data/melitz_polanec/` y texto y figuras bajo `Paper/`. Los microdatos y paneles empresariales están excluidos de Git. El boletín contiene hallazgos iniciales, nota metodológica y pruebas de robustez pendientes.

## Informe agregado original

Borrador de la serie Informes sobre la Productividad en Colombia del Centro Javeriano de Competitividad, con datos anuales de 2005 a 2025.

En Overleaf, el documento principal es `main.tex`. Para compilar localmente, ejecutar `tectonic main.tex` desde la raíz. El documento incluye los cuadros y la figura compilables.

La fuente es el [anexo de productividad laboral del DANE](https://www.dane.gov.co/files/operaciones/PTF/anex-PTF-ProductividadLaboral-2025.xlsx), publicado el 31 de marzo de 2026. `data/productividad_laboral.csv` recoge las 21 observaciones de los cuadros 1 y 2. En el cuadro 2, F se asigna a capital por persona y G a composición laboral. G coincide en todos los años con la composición del cuadro 1. El informe explica la comprobación y la diferencia con los rótulos publicados.

Para reconstruir el CSV, los cuadros y la figura, instalar `openpyxl` y `reportlab` y ejecutar `python scripts/reproducir.py ruta/al/anexo.xlsx`. El script registra la huella SHA-256 y comprueba el cierre de las identidades antes de escribir los resultados.
