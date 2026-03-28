# Force single-threaded execution during tests to avoid CRAN NOTE
# ("CPU time N times elapsed time")
if (requireNamespace("future", quietly = TRUE)) {
  future::plan(future::sequential)
}

# Limit BLAS/OpenMP threads used by NumPy/scipy via reticulate
Sys.setenv(
  OMP_NUM_THREADS = 1,
  OPENBLAS_NUM_THREADS = 1,
  MKL_NUM_THREADS = 1,
  VECLIB_MAXIMUM_THREADS = 1,
  NUMEXPR_NUM_THREADS = 1
)

skip_if_no_pymyami <- function() {
  have_pymyami <- reticulate::py_module_available("pymyami")
  if (!have_pymyami) {
    testthat::skip("pymyami not available for testing")
  }
}
