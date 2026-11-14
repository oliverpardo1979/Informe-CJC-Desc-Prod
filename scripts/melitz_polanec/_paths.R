# Ejecutar desde la raíz del repositorio.
PROJECT_ROOT <- normalizePath(getwd(), winslash="/", mustWork=TRUE)
stopifnot(file.exists(file.path(PROJECT_ROOT, "melitz-polanec.tex")))
SOURCE_ROOT <- Sys.getenv("CJC_SOURCE_ROOT", unset=dirname(PROJECT_ROOT))
project_path <- function(...) file.path(PROJECT_ROOT, ...)
source_path <- function(...) file.path(SOURCE_ROOT, ...)
dir.create(project_path("data", "melitz_polanec", "tables"), recursive=TRUE, showWarnings=FALSE)
