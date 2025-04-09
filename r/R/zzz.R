# Select pyMyAMI version
pymyami_version <- "2.1.0"

.onLoad <- function(...) {
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
