# Force sequential execution during tests to avoid CRAN NOTE
# ("CPU time N times elapsed time" from parallel workers)
if (requireNamespace("future", quietly = TRUE)) {
  future::plan(future::sequential)
}

skip_if_no_pymyami <- function() {
  have_pymyami <- reticulate::py_module_available("pymyami")
  if (!have_pymyami) {
    testthat::skip("pymyami not available for testing")
  }
}
