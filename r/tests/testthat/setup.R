skip_if_no_pymyami <- function() {
  have_pymyami <- reticulate::py_module_available("pymyami")
  if (!have_pymyami) {
    testthat::skip("pymyami not available for testing")
  }
}
