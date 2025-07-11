#' @title Import Kgen coefficients on package load
#'
#' @description Read parameter files used throughout calculation functions.
#'
#' @author Oscar Branson

# Create package environment to store coefficients
.kgen_env <- new.env(parent = emptyenv())

.onLoad <- function(libname, pkgname) {
  # Load K coefficients
  k_data <- rjson::fromJSON(file = system.file("coefficients/K_calculation.json", package = pkgname))
  .kgen_env$K_coefs <- k_data$coefficients
  
  # Load pressure correction coefficients
  pc_data <- rjson::fromJSON(file = system.file("coefficients/K_pressure_correction.json", package = pkgname))
  .kgen_env$K_presscorr_coefs <- pc_data$coefficients
  
  # Load pymyami polynomial coefficients
  .kgen_env$poly_coefs <- rjson::fromJSON(file = system.file("coefficients/polynomial_coefficients.json", package = pkgname))

  invisible()
}
