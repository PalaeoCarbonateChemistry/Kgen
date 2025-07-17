# Create new env to store pkg specific variables in memory
kgen.pkg.env <- new.env()

# Select pyMyAMI version
kgen.pkg.env$pymyami_version <- "2.1.1"

# Load K_calculation.json
kgen.pkg.env$K_coefs <-
  rjson::fromJSON(file = system.file("coefficients/K_calculation.json", package = "kgen"))$coefficients

# Load K_pressure_correction.json
kgen.pkg.env$K_presscorr_coefs <-
  rjson::fromJSON(file = system.file("coefficients/K_pressure_correction.json", package = "kgen"))$coefficients

kgen.pkg.env$poly_coefs <-
  rjson::fromJSON(file = system.file("coefficients/polynomial_coefficients.json", package = "kgen"))

.onLoad <- function(...) {
  reticulate::py_require(paste0("pymyami==", kgen.pkg.env$pymyami_version))
}

.onAttach <- function(lib, pkg) {
  if (methods::is(future::plan(), "sequential")) {
    packageStartupMessage(
      "Kgen v",
      utils::packageDescription("kgen", fields = "Version"),
      paste0(" // pyMyAMI v", kgen.pkg.env$pymyami_version),
      appendLF = TRUE
    )
  }
}
