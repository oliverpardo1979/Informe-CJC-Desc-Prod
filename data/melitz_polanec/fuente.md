# Procedencia y decisiones

Migración local del 13-11-2026 desde `CJC-Monitor/Melitz-Polanec`.

| Fuente | Archivo de entrada en CJC_SOURCE_ROOT | Uso |
|---|---|---|
| EAM, DANE | Datos/Processed/EAC_EAM/EAM_panel_completo.rds | Agregar establecimientos por NORDEMP |
| EAC, DANE | Datos/Processed/EAC_EAM/EAC_panel.rds | Panel de empresas; revisar intercambio AGREGA/VENTA 2017–2018 |
| EAS, DANE | Datos/Raw/EAS/EAS* | Archivos anuales, identificador idnoremp |
| IPP, DANE | Datos/Raw/IPP_DANE/anex-IPP-historicos-sep2026.xlsx | Deflactor industrial común |
| Cuentas departamentales, DANE | Datos/Raw/PIB_DANE/anex-PIBDep-departamento-2024pr.xlsx | Deflactores amplios de comercio y servicios |

Los RDS de esta carpeta son derivados locales excluidos de Git. Las tablas agregadas se conservan para permitir reconstruir el boletín sin redistribuir microdatos. La reproducción completa requiere las fuentes locales y las dependencias indicadas en `scripts/melitz_polanec/README.md`. No se hizo una nueva descarga ni auditoría de fuentes durante la migración.
