# Descomposición de la productividad laboral en Colombia

Borrador de la serie Informes sobre la Productividad en Colombia del Centro Javeriano de Competitividad, con datos anuales de 2005 a 2025.

En Overleaf, el documento principal es `main.tex`. Para compilar localmente, ejecutar `tectonic main.tex` desde la raíz. El documento incluye los cuadros y la figura compilables.

La fuente es el [anexo de productividad laboral del DANE](https://www.dane.gov.co/files/operaciones/PTF/anex-PTF-ProductividadLaboral-2025.xlsx), publicado el 31 de marzo de 2026. `data/productividad_laboral.csv` recoge las 21 observaciones de los cuadros 1 y 2. En el cuadro 2, F se asigna a capital por persona y G a composición laboral. G coincide en todos los años con la composición del cuadro 1. El informe explica la comprobación y la diferencia con los rótulos publicados.

Para reconstruir el CSV, los cuadros y la figura, instalar `openpyxl` y `reportlab` y ejecutar `python scripts/reproducir.py ruta/al/anexo.xlsx`. El script registra la huella SHA-256 y comprueba el cierre de las identidades antes de escribir los resultados.
