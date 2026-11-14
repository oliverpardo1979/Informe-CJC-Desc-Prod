# Descomposicion dinamica de Olley-Pakes (Melitz y Polanec, 2015) de la productividad laboral con la EAC (comercio) y la EAS (servicios).
#
# Misma descomposicion que 04_DOPD_productividad_laboral.R (EAM): unidad = empresa, phi = log(valor agregado real / personal), participaciones de empleo,
# DOPD (ecuacion 6) y, para comparar, Griliches-Regev (GR) y Foster-Haltiwanger-Krizan (FHK). Puntos logaritmicos x 100.
#   sobreviviente = en la muestra en t1 y en t2; entrante = solo en t2; saliente = solo en t1.
# Ventanas:
#   EAC: 2015-2019 y 2020-2024 (el identificador de empresa cambia en 2020: no se pueden seguir empresas de 2019 a 2024); 2010-2015 y 2005-2010 se reportan aparte
#        (el universo de la EAC se amplia en 2014 y antes de 2013 mezcla estratos muestrales: las "entradas" no son nacimientos).
#   EAS: 2010-2015, 2015-2019 y 2019-2024; 2006-2010 aparte (comparable = FALSE, igual que 2005-2010 en la EAM).
# Entradas: data/melitz_polanec/panel_empresas_EAC.rds y panel_empresas_EAS.rds (07_panel_empresas_EAC_EAS.R)
# Salidas : Outputs/tables/dopd_laboral_ventanas_comercio_servicios.csv (componentes), dopd_laboral_comparacion_comercio_servicios.csv (DOPD vs GR vs FHK),
#           dopd_laboral_grupos_comercio_servicios.csv (tamanos de los grupos)
# Uso    : Rscript scripts/melitz_polanec/08_DOPD_comercio_servicios.R   (desde la raiz del repositorio)

source("scripts/melitz_polanec/_paths.R")
setwd(PROJECT_ROOT)
suppressMessages(library(dplyr))
dir_out <- project_path("data", "melitz_polanec", "tables")

# ---- funcion (identica a la de 04_DOPD_productividad_laboral.R) ------------------------------------------------------------
descomponer <- function(d1, d2) {
  d1$s <- d1$w / sum(d1$w); d2$s <- d2$w / sum(d2$w)
  S <- intersect(d1$id, d2$id)
  a1 <- d1[d1$id %in% S, ]; a2 <- d2[d2$id %in% S, ]
  a1 <- a1[order(a1$id), ]; a2 <- a2[order(a2$id), ]
  stopifnot(identical(a1$id, a2$id))
  e2 <- d2[!d2$id %in% S, ]; x1 <- d1[!d1$id %in% S, ]
  Phi1 <- sum(d1$s * d1$phi); Phi2 <- sum(d2$s * d2$phi)
  grp <- function(d) { sG <- sum(d$s); w <- d$s / sG; list(sG = sG, Phi = sum(w * d$phi), media = mean(d$phi), cov = sum(w * d$phi) - mean(d$phi), n = nrow(d)) }
  S1 <- grp(a1); S2 <- grp(a2); E2 <- grp(e2); X1 <- grp(x1)
  dopd <- c(dentro_media_sobrevivientes = S2$media - S1$media, reasignacion_covarianza_sobrevivientes = S2$cov - S1$cov,
            entrada = E2$sG * (E2$Phi - S2$Phi), salida = X1$sG * (S1$Phi - X1$Phi))
  Pm <- (Phi1 + Phi2) / 2; sb <- (a1$s + a2$s) / 2; pb <- (a1$phi + a2$phi) / 2
  gr <- c(dentro = sum(sb * (a2$phi - a1$phi)), entre = sum((a2$s - a1$s) * (pb - Pm)), entrada = sum(e2$s * (e2$phi - Pm)), salida = sum(x1$s * (Pm - x1$phi)))
  fhk <- c(dentro = sum(a1$s * (a2$phi - a1$phi)), entre = sum((a2$s - a1$s) * (a1$phi - Phi1)), cruzado = sum((a2$s - a1$s) * (a2$phi - a1$phi)),
           entrada = sum(e2$s * (e2$phi - Phi1)), salida = sum(x1$s * (Phi1 - x1$phi)))
  tot <- Phi2 - Phi1
  stopifnot(abs(sum(dopd) - tot) < 1e-9, abs(sum(gr) - tot) < 1e-9, abs(sum(fhk) - tot) < 1e-9)
  list(Phi1 = Phi1, Phi2 = Phi2, total = tot, dopd = dopd, gr = gr, fhk = fhk,
       grupos = c(n1 = nrow(d1), n2 = nrow(d2), sobrevivientes = S1$n, entrantes = E2$n, salientes = X1$n,
                  s_entrantes_t2 = E2$sG, s_salientes_t1 = X1$sG, Phi_S1 = S1$Phi, Phi_S2 = S2$Phi, Phi_E2 = E2$Phi, Phi_X1 = X1$Phi))
}

# ---- pruebas: sin entrada ni salida y crecimiento uniforme; ejemplo del articulo --------------------------------------------
set.seed(1); n <- 500
t1 <- data.frame(id = 1:n, phi = rnorm(n), w = runif(n, 1, 50)); t2 <- transform(t1, phi = phi + 0.10)
r0 <- descomponer(t1, t2)
stopifnot(abs(r0$dopd[["entrada"]]) < 1e-12, abs(r0$dopd[["salida"]]) < 1e-12, abs(r0$total - 0.10) < 1e-12)
g <- 0.10; d1 <- data.frame(id = 1:270, phi = 1, w = 1); d2 <- data.frame(id = c(1:270, 301:330), phi = 1 + g, w = 1)
r1 <- descomponer(d1, d2)
stopifnot(abs(r1$dopd[["entrada"]]) < 1e-12, abs(r1$dopd[["salida"]]) < 1e-12, r1$gr[["entrada"]] > 0)
cat("Pruebas de identidad y del ejemplo del articulo: ok\n")

# ---- datos reales -------------------------------------------------------------------------------------------------------------
paneles <- list(
  EAC = list(p = readRDS(project_path("data", "melitz_polanec", "panel_empresas_EAC.rds")),
             ventanas = list(c(2010, 2015, FALSE), c(2015, 2019, TRUE), c(2020, 2024, TRUE), c(2005, 2010, FALSE))),
  EAS = list(p = readRDS(project_path("data", "melitz_polanec", "panel_empresas_EAS.rds")),
             ventanas = list(c(2010, 2015, TRUE), c(2015, 2019, TRUE), c(2019, 2024, TRUE), c(2006, 2010, FALSE))))
filas <- list(); comp <- list(); grup <- list()
for (enc in names(paneles)) {
  p <- paneles[[enc]]$p %>% filter(muestra)
  for (v in paneles[[enc]]$ventanas) {
    d1 <- p %>% filter(anio == v[1]) %>% transmute(id, phi, w = l); d2 <- p %>% filter(anio == v[2]) %>% transmute(id, phi, w = l)
    r <- descomponer(d1, d2); lab <- paste0(v[1], "-", v[2]); comparable <- as.logical(v[3]); tot <- r$total
    k <- paste(enc, lab)
    filas[[k]] <- data.frame(encuesta = enc, ventana = lab, comparable = comparable, Phi_inicial = 100 * r$Phi1, Phi_final = 100 * r$Phi2, cambio_total = 100 * tot,
                             componente = names(r$dopd), valor_pp = 100 * r$dopd, pct_del_cambio = 100 * r$dopd / tot)
    comp[[k]] <- data.frame(encuesta = enc, ventana = lab, comparable = comparable, cambio_total = 100 * tot,
                            DOPD_entrada = 100 * r$dopd[["entrada"]], GR_entrada = 100 * r$gr[["entrada"]], FHK_entrada = 100 * r$fhk[["entrada"]],
                            DOPD_salida = 100 * r$dopd[["salida"]], GR_salida = 100 * r$gr[["salida"]], FHK_salida = 100 * r$fhk[["salida"]],
                            DOPD_reasignacion = 100 * r$dopd[["reasignacion_covarianza_sobrevivientes"]], GR_entre = 100 * r$gr[["entre"]], FHK_entre = 100 * (r$fhk[["entre"]] + r$fhk[["cruzado"]]))
    grup[[k]] <- data.frame(encuesta = enc, ventana = lab, comparable = comparable, t(round(r$grupos, 4)))
  }
}
res <- bind_rows(filas); cmp <- bind_rows(comp); gru <- bind_rows(grup)
write.csv(res, file.path(dir_out, "dopd_laboral_ventanas_comercio_servicios.csv"), row.names = FALSE)
write.csv(cmp, file.path(dir_out, "dopd_laboral_comparacion_comercio_servicios.csv"), row.names = FALSE)
write.csv(gru, file.path(dir_out, "dopd_laboral_grupos_comercio_servicios.csv"), row.names = FALSE)
options(width = 220)
cat("\n== Grupos\n"); print(gru, row.names = FALSE)
cat("\n== DOPD (puntos log x 100)\n")
print(res %>% select(encuesta, ventana, comparable, cambio_total, componente, valor_pp, pct_del_cambio) %>% mutate(across(where(is.numeric), ~ round(.x, 2))), row.names = FALSE)
cat("\n== DOPD frente a GR y FHK\n"); print(cmp %>% mutate(across(where(is.numeric), ~ round(.x, 2))), row.names = FALSE)
