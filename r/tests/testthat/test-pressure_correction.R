testthat::test_that("Test that the pressure correction produces expected results...", {
  exp_val <- rjson::fromJSON(file = system.file("check_values/check_presscorr.json", package = "kgen"))
  press_cor <- mapply(function(k) {
    calc_pressure_correction(
      k = k, temp_c = exp_val$input_conditions$TC,
      p_bar = exp_val$input_conditions$P
    )
  }, names(exp_val$check_values))

  testthat::expect_equal(exp_val$check_values, as.list(press_cor), tolerance = 1E-3)
})
