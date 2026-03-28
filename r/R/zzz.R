# Create new env to store pkg specific variables in memory
kgen.pkg.env <- new.env()

# Select pyMyAMI version
kgen.pkg.env$pymyami_version <- "2.1.3"
kgen.pkg.env$pymyami_ready <- FALSE

#' Ensure pymyami Python package is available (called lazily on first use)
#' @noRd
ensure_pymyami <- function() {
  if (!kgen.pkg.env$pymyami_ready) {
    reticulate::py_require(paste0("pymyami==", kgen.pkg.env$pymyami_version))
    kgen.pkg.env$pymyami_ready <- TRUE
  }
}

.onLoad <- function(...) {
  # Load coefficients at load time when system.file() can resolve paths
  kgen.pkg.env$K_coefs <-
    rjson::fromJSON(file = system.file("coefficients/K_calculation.json", package = "kgen"))$coefficients

  kgen.pkg.env$K_presscorr_coefs <-
    rjson::fromJSON(file = system.file("coefficients/K_pressure_correction.json", package = "kgen"))$coefficients

  kgen.pkg.env$poly_coefs <-
    rjson::fromJSON(file = system.file("coefficients/polynomial_coefficients.json", package = "kgen"))
}

.onAttach <- function(lib, pkg) {
  packageStartupMessage(
    "Kgen v",
    utils::packageDescription("kgen", fields = "Version"),
    paste0(" // pyMyAMI v", kgen.pkg.env$pymyami_version),
    appendLF = TRUE
  )
}
