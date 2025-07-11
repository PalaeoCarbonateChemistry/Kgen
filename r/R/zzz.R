# Select pyMyAMI version
pymyami_version <- "2.1.1"

.kgen_env <- new.env(parent = emptyenv())

.onLoad <- function(...) {
  # Load K coefficients
  k_data <- rjson::fromJSON(file = system.file("coefficients/K_calculation.json", package = "kgen"))
  .kgen_env$K_coefs <- k_data$coefficients
  
  # Load pressure correction coefficients
  pc_data <- rjson::fromJSON(file = system.file("coefficients/K_pressure_correction.json", package = "kgen"))
  .kgen_env$K_presscorr_coefs <- pc_data$coefficients
  
  # Load pymyami polynomial coefficients
  .kgen_env$poly_coefs <- rjson::fromJSON(file = system.file("coefficients/polynomial_coefficients.json", package = "kgen"))

  reticulate::py_require(paste0("pymyami==", pymyami_version))
  pymyami <<- reticulate::import("pymyami", delay_load = TRUE)
}

.onAttach <- function(lib, pkg) {
  packageStartupMessage(
    "Kgen v",
    utils::packageDescription("kgen",
      fields = "Version"
    ),
    paste0(" // pyMyAMI v", pymyami_version),
    appendLF = TRUE
  )
}
