# Paneles de EMPRESAS de la EAC (comercio) y de la EAS (servicios) para la descomposicion de la productividad laboral de Melitz y Polanec.
#
# A diferencia de la EAM, las dos encuestas ya son de empresas: la unidad es la empresa (IDNOREMP). No traen capital, asi que la muestra exige solo valor agregado > 0 y personal > 0.
# EAC (Encuesta Anual de Comercio): valor agregado AGREGA, personal ocupado TOTPERSO. Fuente armonizada: Datos/Processed/EAC_EAM/EAC_panel.rds (2003-2024; se usa desde 2005, que es donde empieza el deflactor).
#   Rupturas del identificador: 2003 -> 2004 (sin solape), 2014 (el archivo no trae identificador) y 2019 -> 2020 (esquema nuevo, sin solape). Por eso no se pueden seguir empresas
#   de 2019 a 2024: la ventana reciente es 2020 -> 2024. Hasta 2012 la encuesta combina un estrato de inclusion forzosa (FACEXP = 1) con estratos muestrales (FACEXP > 1); como el universo
#   se amplia en 2014 (de ~7.000 a ~10.600 empresas), la ventana 2010 -> 2015 no es comparable y se reporta aparte. En 2010-2012 se usa solo FACEXP = 1.
# EAS (Encuesta Anual de Servicios): valor agregado VALAGRE, personal ocupado PEROCU (si falta, POTTOT). Archivos crudos 2006-2024 (sav y dta). El identificador es continuo en todos los anos.
# Aviso de calidad: en los archivos de 2017 y 2018 de la EAC las columnas AGREGA y VENTA estan intercambiadas (el cociente de AGREGA con el año anterior es 6,5 y el de VENTA 0,14, y en 2019 se revierte);
#   aqui se intercambian de nuevo. Ningun otro codigo del repositorio usa AGREGA de la EAC.
# Deflactor: valor agregado implicito de comercio (EAC) y de servicios (EAS), 2015 = 1 (data/melitz_polanec/deflactores_comercio_servicios_anual.csv).
# Productividad: phi_it = log(valor agregado real / personal).
#
# Salidas: data/melitz_polanec/panel_empresas_EAC.rds, panel_empresas_EAS.rds  y  Outputs/tables/panel_empresas_EAC_EAS_resumen_anual.csv
# Uso    : Rscript scripts/melitz_polanec/07_panel_empresas_EAC_EAS.R   (desde la raiz del repositorio)

source("scripts/melitz_polanec/_paths.R")
setwd(PROJECT_ROOT)
suppressMessages({library(dplyr); library(haven)})
dir_dat <- project_path("data", "melitz_polanec"); dir_out <- project_path("data", "melitz_polanec", "tables")
defl <- read.csv(file.path(dir_dat, "deflactores_comercio_servicios_anual.csv"))

# ---- EAC
eac <- readRDS(source_path("Datos", "Processed", "EAC_EAM", "EAC_panel.rds")) %>%
  transmute(anio = as.integer(ANIO), id = as.character(IDNOREMP), va = as.numeric(AGREGA), venta = as.numeric(VENTA), l = as.numeric(TOTPERSO), facexp = as.numeric(FACEXP)) %>%
  mutate(va = ifelse(anio %in% 2017:2018, venta, va)) %>%                 # en 2017 y 2018 las columnas AGREGA y VENTA del archivo estan intercambiadas (ver nota del encabezado)
  filter(anio >= 2005, anio != 2014, !is.na(id)) %>%                                  # 2014 no trae identificador
  mutate(estrato_censal = is.na(facexp) | facexp == 1) %>%
  left_join(defl %>% select(anio, deflactor = defl_comercio), by = "anio") %>%
  mutate(muestra = va > 0 & l > 0 & estrato_censal, va_real = va / deflactor, phi = ifelse(muestra, log(pmax(va_real, 1e-9) / pmax(l, 1e-9)), NA_real_))
stopifnot(!anyDuplicated(eac[, c("anio", "id")]), !any(is.na(eac$deflactor)))
saveRDS(eac, file.path(dir_dat, "panel_empresas_EAC.rds"))

# ---- EAS: lectura de los archivos crudos
leer_eas <- function(f) {
  rd <- if (grepl("\\.sav$", f, ignore.case = TRUE)) haven::read_sav else haven::read_dta
  d <- rd(f); names(d) <- tolower(names(d))
  anio <- as.integer(regmatches(basename(f), regexpr("[0-9]{4}", basename(f))))
  tibble(anio = anio, id = as.character(as.numeric(d$idnoremp)), va = as.numeric(d$valagre), perocu = as.numeric(d$perocu), pottot = as.numeric(d$pottot))
}
archivos <- list.files(source_path("Datos", "Raw", "EAS"), pattern = "^EAS", full.names = TRUE)
eas <- bind_rows(lapply(archivos, leer_eas)) %>%
  group_by(anio, id) %>% summarise(va = sum(va, na.rm = TRUE), perocu = sum(perocu, na.rm = TRUE), pottot = sum(pottot, na.rm = TRUE), .groups = "drop") %>%      # unas pocas filas repetidas (2013): se suman
  mutate(l = ifelse(!is.na(perocu) & perocu > 0, perocu, pottot)) %>%
  left_join(defl %>% select(anio, deflactor = defl_servicios), by = "anio") %>%
  mutate(muestra = va > 0 & l > 0, va_real = va / deflactor, phi = ifelse(muestra, log(pmax(va_real, 1e-9) / pmax(l, 1e-9)), NA_real_))
stopifnot(!anyDuplicated(eas[, c("anio", "id")]), !any(is.na(eas$deflactor)), setequal(unique(eas$anio), 2006:2024))
saveRDS(eas, file.path(dir_dat, "panel_empresas_EAS.rds"))

resumen <- function(p, nombre) p %>% group_by(anio) %>% summarise(
  encuesta = nombre, empresas = n(), empresas_muestra = sum(muestra), pct_muestra = round(100 * mean(muestra), 1),
  personal_muestra = sum(l[muestra]), va_real_millones_2015 = round(sum(va_real[muestra]) / 1e3),
  phi_p1 = quantile(phi, .01, na.rm = TRUE), phi_mediana = median(phi, na.rm = TRUE), phi_p99 = quantile(phi, .99, na.rm = TRUE), .groups = "drop") %>%
  mutate(across(starts_with("phi"), ~ round(.x, 2)))
res <- bind_rows(resumen(eac, "EAC"), resumen(eas, "EAS"))
write.csv(res, file.path(dir_out, "panel_empresas_EAC_EAS_resumen_anual.csv"), row.names = FALSE)
options(width = 200); print(as.data.frame(res), row.names = FALSE)
# continuidad de identificadores en las ventanas
ov <- function(p, a, b) { A <- p$id[p$anio == a & p$muestra]; B <- p$id[p$anio == b & p$muestra]; c(a = a, b = b, n_a = length(A), n_b = length(B), en_ambos = length(intersect(A, B)), pct_a_sigue = round(100 * length(intersect(A, B)) / length(A), 1)) }
cat("\nEAC:\n"); print(rbind(ov(eac, 2010, 2015), ov(eac, 2015, 2019), ov(eac, 2020, 2024), ov(eac, 2019, 2020)))
cat("\nEAS:\n"); print(rbind(ov(eas, 2010, 2015), ov(eas, 2015, 2019), ov(eas, 2019, 2024), ov(eas, 2006, 2010)))
