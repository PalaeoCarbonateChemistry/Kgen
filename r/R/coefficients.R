K_coefs <- NULL
K_presscorr_coefs <- NULL
poly_coefs <- NULL

.onLoad <- function(libname, pkgname) {
  # Load K coefficients
  K_coefs <<- rjson::fromJSON(file = system.file("coefficients/K_calculation.json", package = "kgen"))
  K_coefs <<- K_coefs$coefficients
  
  # Load pressure correction coefficients
  K_presscorr_coefs <<- rjson::fromJSON(file = system.file("coefficients/K_pressure_correction.json", package = "kgen"))
  K_presscorr_coefs <<- K_presscorr_coefs$coefficients
  
  # Load pymyami polynomial coefficients
  poly_coefs <- rjson::fromJSON(file = system.file("coefficients/polynomial_coefficients.json", package = "kgen"))

  invisible()
}