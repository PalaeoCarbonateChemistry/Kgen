testthat::test_that("Test that R_Polynomial produces expected results...", {
  exp_val <- rjson::fromJSON(file = system.file("check_values/check_Ks.json", package = "kgen"))
  calc_val <- calc_Ks(temp_c = exp_val$input_conditions$TC, sal = exp_val$input_conditions$S, method = "R_Polynomial")

  testthat::expect_equal(exp_val$check_values, as.list(log(calc_val)), tolerance = 1E-3)
})

testthat::test_that("Test that MyAMI_Polynomial produces expected results...", {
  skip_if_no_pymyami()

  exp_val <- rjson::fromJSON(file = system.file("check_values/check_Ks.json", package = "kgen"))
  calc_val <- calc_Ks(temp_c = exp_val$input_conditions$TC, sal = exp_val$input_conditions$S, method = "MyAMI_Polynomial")

  testthat::expect_equal(exp_val$check_values, as.list(log(calc_val)), tolerance = 1E-3)
})

testthat::test_that("Test that MyAMI produces expected results...", {
  skip_if_no_pymyami()

  exp_val <- rjson::fromJSON(file = system.file("check_values/check_Ks.json", package = "kgen"))
  calc_val <- calc_Ks(temp_c = exp_val$input_conditions$TC, sal = exp_val$input_conditions$S, method = "MyAMI")

  testthat::expect_equal(exp_val$check_values, as.list(log(calc_val)), tolerance = 1E-3)
})
