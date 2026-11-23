# Literatura para el boletín empresarial

Corte: 22 de noviembre de 2026. Veinte referencias formales: once artículos publicados, un capítulo, siete informes (uno preliminar) y un documento de trabajo institucional. Revisión dirigida, no sistemática ni exhaustiva.

Prioridad: América Latina; Eslovenia, Francia y Corea ofrecen contrastes metodológicos. Se distingue el estatus editorial de la versión efectivamente leída. Brown et al. solo se utiliza desde su resumen; el texto consultado de César y Falcone es una versión de autor anterior a la publicación.

| Referencia | País | Tipo | Alcance de lectura |
|---|---|---|---|
| [melitz2015](fichas/melitz2015.md) | Eslovenia | Artículo publicado | Texto del artículo, metodología y resultados |
| [ifc2022](fichas/ifc2022.md) | Chile | Informe institucional | Capítulo 3.1; tabla y notas |
| [cesar2020](fichas/cesar2020.md) | Chile | Artículo publicado; copia de autor anterior | Publicación verificada en JSTOR; apéndice de versión de autor diciembre 2019 |
| [brown2018](fichas/brown2018.md) | Chile; Colombia; México; Perú | Artículo publicado | Solo resumen editorial y notas públicas; acceso completo restringido |
| [wb2024](fichas/wb2024.md) | Colombia | Informe institucional | Sección 4.3 y anexo 9; no libro completo |
| [imf2025](fichas/imf2025.md) | Brasil; Colombia; México y comparadores | Informe institucional | Capítulo 2 y notas 7-8; anexo en línea no revisado |
| [benhassine2019](fichas/benhassine2019.md) | Francia | Artículo publicado | Texto, metodología y nota 16 |
| [song2021](fichas/song2021.md) | Corea del Sur | Artículo publicado | Artículo abierto: introducción, método y resultados |
| [eslava2004](fichas/eslava2004.md) | Colombia | Artículo publicado | Resumen institucional; publicación verificada; no lectura integral |
| [eslava2006](fichas/eslava2006.md) | Colombia | Artículo publicado | Resumen y primera página del artículo institucional |
| [foster2001](fichas/foster2001.md) | Estados Unidos | Capítulo publicado | Resumen NBER y discusión del capítulo, página 312 |
| [pancost2022](fichas/pancost2022.md) | Estados Unidos | Documento de trabajo institucional | Resumen institucional; no lectura integral |
| [olley1996](fichas/olley1996.md) | Estados Unidos | Artículo publicado | Resumen NBER y registro de publicación |
| [griliches1995](fichas/griliches1995.md) | Israel | Artículo publicado | Resumen editorial |
| [bartelsman2013](fichas/bartelsman2013.md) | Varios países | Artículo publicado | Resumen editorial y primera página del artículo |
| [mexico2021](fichas/mexico2021.md) | México | Informe institucional | Capítulo 3, figura 3.3; anexo 3A consultado parcialmente |
| [colombia2024](fichas/colombia2024.md) | Colombia | Informe institucional | Resumen institucional, sección de descomposición y notas visibles en versión web |
| [portugal2022](fichas/portugal2022.md) | Portugal | Informe institucional | Resultados y notas técnicas del capítulo web |
| [harris2019](fichas/harris2019.md) | Reino Unido | Artículo publicado; copia de autor | Versión de autor: resumen, ecuaciones y tabla 4; publicación verificada en Durham |
| [opce2024](fichas/opce2024.md) | España | Informe institucional preliminar | Recuadro 4.2 y portada; no se extraen resultados agregados |

## Organización

`referencias.json` es el catálogo maestro; `referencias.bib` permite reutilizar las citas. `fichas/` registra hallazgos y límites. `pdf/` guarda copias locales de acceso abierto, excluidas de Git; `descargas.json` registra URL, fecha y huella SHA-256. Para recuperarlas: `python scripts/melitz_polanec/literatura.py --download`. No se intenta eludir accesos de pago.

## Cómo usar la comparación

Comparar primero método, medida (PTF o laboral), pesos, empresa o establecimiento, periodo, deflactor y cobertura. Por ahora el boletín contrasta mecanismos y signos, no construye un ranking internacional de magnitudes. El estudio de Colombia del Banco Mundial es una prueba pendiente de reconciliación, no una validación de nuestros resultados.

## Búsqueda y exclusiones

Búsquedas combinando Melitz, Polanec, productividad y Chile/Colombia/Brasil; rastreo de referencias y fuentes editoriales e institucionales. Se excluyeron blogs, diapositivas y resultados sin fuente formal identificable. García-Marín (2021) se conoce a través de IFC: no se presenta como documento leído ni como artículo arbitrado. El informe FMI combina GR y MP. No se confirma la implementación exacta de Brown et al. sin acceso al artículo completo.

## Siguientes lecturas

Conseguir el texto completo de Brown et al. y el informe técnico de García-Marín; revisar el anexo en línea del FMI; ampliar países latinoamericanos sin relajar los criterios de verificabilidad.
