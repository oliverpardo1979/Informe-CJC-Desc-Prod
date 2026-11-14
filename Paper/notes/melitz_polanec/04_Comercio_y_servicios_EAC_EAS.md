> Nota histórica migrada el 13 de noviembre de 2026. Para rutas y estado vigentes, consultar `scripts/melitz_polanec/README.md` desde la raíz del repositorio.

# Descomposición de Melitz–Polanec con la EAC (comercio) y la EAS (servicios)

Fecha: 2026-11-09. Mismo ejercicio que la EAM ([`03_Etapas_1-3_Productividad_laboral.md`](03_Etapas_1-3_Productividad_laboral.md)): productividad laboral, `log(valor agregado real / personal)`, participaciones de empleo, unidad = empresa.
Código: [`06_deflactores_comercio_servicios.py`](../Code/06_deflactores_comercio_servicios.py), [`07_panel_empresas_EAC_EAS.R`](../Code/07_panel_empresas_EAC_EAS.R), [`08_DOPD_comercio_servicios.R`](../Code/08_DOPD_comercio_servicios.R), [`09_figura_DOPD_comercio_servicios.py`](../Code/09_figura_DOPD_comercio_servicios.py).
Figuras: `../Outputs/Figures/fig_dopd_laboral_EAC.png` y `fig_dopd_laboral_EAS.png`. Tablas: `../Outputs/tables/*_comercio_servicios.csv`.

## Datos y decisiones
| | EAC (comercio) | EAS (servicios) |
|---|---|---|
| Unidad | Empresa (`IDNOREMP`; ya es de empresas, no hay que agregar establecimientos) | Empresa (`idnoremp`) |
| Valor agregado / personal | `AGREGA` / `TOTPERSO` | `VALAGRE` / `PEROCU` (si falta, `POTTOT`) |
| Empresas por año | 7.000–10.600 | 3.900–6.900 |
| Muestra | VA > 0 y personal > 0 (y estrato de inclusión forzosa antes de 2013) | VA > 0 y personal > 0 |
| Deflactor | Valor agregado implícito de comercio, transporte y alojamiento | Valor agregado implícito de información, profesionales y apoyo, administración pública, educación y salud, y otros servicios |
| Ventanas | 2015→2019 y 2020→2024; 2010→2015 y 2005→2010 aparte | 2010→2015, 2015→2019, 2019→2024; 2006→2010 aparte |

Ni la EAC ni la EAS traen capital, así que solo se puede hacer productividad laboral (no PTF).
El deflactor sale del PIB departamental 2005–2024pr (corrientes y volumen encadenado, suma de los 33 departamentos), con 2015 = 1. Es común a todas las empresas de cada encuesta: solo desplaza el componente "dentro de las empresas".

## Problemas de los datos que se resolvieron o se reportan
1. **EAC 2017 y 2018: `AGREGA` y `VENTA` están intercambiadas.** El cociente de `AGREGA` frente al año anterior es 6,5 (y 0,14 el de `VENTA`) y se revierte en 2019. El panel las intercambia de nuevo. Ningún otro código del repositorio usa `AGREGA` de la EAC.
2. **EAC: el identificador de empresa se rompe** en 2003→2004, en 2014 (el archivo no trae identificador) y en 2019→2020 (esquema nuevo, solapamiento 0%). Por eso no se pueden seguir empresas de 2019 a 2024 y la ventana reciente es **2020→2024** (2020 es año de pandemia). Posible puente: el inventario inicial de un año es igual al final del anterior; no se hizo.
3. **EAC: el universo cambia.** Hasta 2012 mezcla un estrato de inclusión forzosa (`FACEXP` = 1) con estratos muestrales (`FACEXP` > 1, con valores no enteros de personal); en 2014 pasa de unas 7.000 a unas 10.600 empresas. La ventana 2010→2015 incluye 5.500 "entrantes" que son parte de esa ampliación: **no es comparable**.
4. **EAS:** identificador continuo en todos los años (solapamiento anual de 95% o más). En 2013 hay 2 filas repetidas, que se suman.
5. Como en la EAM, entrada y salida incluyen empresas que cruzan el umbral de cobertura; no son nacimientos y cierres.

## Resultados (puntos logarítmicos × 100)
| Encuesta | Ventana | Cambio total | Dentro de las empresas | Reasignación entre sobrevivientes | Entrada | Salida |
|---|---|---|---|---|---|---|
| EAC | 2015→2019 | −0,9 | −10,9 | +7,8 | −0,4 | +2,7 |
| EAC | 2020→2024 | +8,7 | +1,8 | +2,5 | +0,5 | +3,9 |
| EAC | 2010→2015 (no comparable) | −15,4 | −8,5 | −7,1 | −4,1 | +4,4 |
| EAS | 2010→2015 | +3,5 | −4,2 | +3,8 | +0,1 | +3,8 |
| EAS | 2015→2019 | +6,4 | −2,4 | +8,0 | 0,0 | +0,7 |
| EAS | 2019→2024 | +13,4 | +8,4 | +6,9 | −3,7 | +1,8 |

Lectura (con cautela):
- **La reasignación entre sobrevivientes pesa en casi todas las ventanas**, igual que en la EAM: en servicios 3,8, 8,0 y 6,9 puntos; en comercio 7,8 y 2,5 en las ventanas comparables.
- **En 2015→2019 el comercio no mejoró: el cambio total fue −0,9.** La caída de la empresa promedio (−10,9) se compensó con reasignación y salida. Parte de la caída "dentro" viene del deflactor: el deflactor de comercio sube 22 puntos logarítmicos en esos años y desplaza solo ese componente.
- **La entrada resta en servicios 2019→2024 (−3,7)**, mucho más que en la EAM. Las nuevas empresas de la EAS entran con menor productividad que las sobrevivientes.
- **La DOPD asigna a la entrada valores más bajos (más negativos) que GR y FHK** en 4 de las 5 ventanas comparables, como en el artículo y en la EAM. En la quinta, EAC 2015→2019, los tres métodos coinciden (−0,45 a −0,47).

## Qué falta
- Robustez (etapa 4): definición estricta de entrante y saliente, recorte de extremos, deflactores por rama, y el puente de identificadores de la EAC 2019→2020.
- Tamaño mínimo de empresa común a las tres encuestas, para comparar industria, comercio y servicios.
