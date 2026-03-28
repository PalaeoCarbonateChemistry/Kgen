#' @title Calculate pressure correction factor
#'
#' @description Calculate pressure correction factor for a specified equilibrium constant.
#'
#' @author Dennis Mayk
#'
#' @inheritParams calc_K1
#' @param k K to be calculated
#' @param p_bar Pressure (Bar)
#' @return pressure correction factor
#' @examples
#' calc_pressure_correction("K1", temp_c = 25, p_bar = 100)
#' @export
calc_pressure_correction <- function(k, temp_c, p_bar) {
  checkmate::assert(
    combine = "and",
    checkmate::check_character(k)
  )

  if (!checkmate::test_numeric(temp_c, lower = 0, upper = 40)) {
    warning("temp_c is outside the recommended range [0, 40].")
  }

  out <-
    calc_pc(
      coefficients = kgen.pkg.env$K_presscorr_coefs[[k]],
      p_bar = p_bar,
      temp_c = temp_c
    )

  return(out)
}

#' @title Kgen R polynomial function
#'
#' @author Dennis Mayk
#'
#' @inheritParams calc_K1
#' @param magnesium Magnesium concentration in mol/kgsw. Default is modern seawater (0.0528171). Should be the average magnesium concentration in seawater - a salinity correction is then applied to calculate the magnesium concentration in the sample.
#' @param calcium Calcium concentration in mol/kgsw. Default is modern seawater (0.0102821). Should be the average calcium concentration in seawater - a salinity correction is then applied to calculate the calcium concentration in the sample.
kgen_poly <- function(sal, temp_c, magnesium = 0.0528171, calcium = 0.0102821) {
  # Ensure all inputs are the same length
  n <- length(sal)
  if (length(temp_c) != n) temp_c <- rep(temp_c, length.out = n)
  if (length(magnesium) != n) magnesium <- rep(magnesium, length.out = n)
  if (length(calcium) != n) calcium <- rep(calcium, length.out = n)

  temp_k <- temp_c + 273.15

  dx <- cbind(temp_k, log(temp_k), sal, magnesium, calcium)
  dy <- stats::poly(dx, degree = 3, raw = TRUE)

  # Add intercept column (all 1s) and reorder columns
  # Sort by index - according to python output
  col_order <- order(-attr(dy, "degree"), colnames(dy), decreasing = TRUE)
  dy_ordered <- dy[, col_order, drop = FALSE]

  # Add intercept column at the beginning
  out <- cbind(1, dy_ordered)

  return(out)
}

#' @title Kgen seawater composition correction function
#'
#' @author Dennis Mayk
#'
#' @inheritParams kgen_poly
#' @param k K to be calculated
#' @param method string describing method which should be either 'myami', 'myami_polynomial', or 'r_polynomial' (Default: 'r_polynomial').
#' @return list of seawater correction factors
#' @examples
#' calc_seawater_correction("K1", sal = 35, temp_c = 25)
#' @export
calc_seawater_correction <-
  function(k,
           sal,
           temp_c,
           magnesium = 0.0528171,
           calcium = 0.0102821,
           method = "r_polynomial") {
    checkmate::assert_choice(tolower(method),
      choices = c("myami", "myami_polynomial", "r_polynomial")
    )

    # Calculate correction factor
    if (tolower(method) %in% c("myami", "myami_polynomial")) {
      ensure_pymyami()
      pymyami <- reticulate::import("pymyami", delay_load = FALSE)
    }

    if (tolower(method) == "myami") {
      seawater_correction <-
        pymyami$calculate_seawater_correction(
          Sal = sal,
          TempC = temp_c,
          Mg = magnesium,
          Ca = calcium
        )
    }
    if (tolower(method) == "myami_polynomial") {
      seawater_correction <-
        pymyami$approximate_seawater_correction(
          Sal = sal,
          TempC = temp_c,
          Mg = magnesium,
          Ca = calcium
        )
    }
    if (tolower(method) == "r_polynomial") {
      # Calculate correction factors
      seawater_correction <- NULL
      if (k %in% names(kgen.pkg.env$poly_coefs)) {
        # Vectorized computation - no more sapply!
        poly_matrix <- kgen_poly(
          sal = sal,
          temp_c = temp_c,
          magnesium = magnesium,
          calcium = calcium
        )

        # Matrix multiplication: each row of poly_matrix multiplied by coefficients
        # This gives us a vector of results for all input combinations
        seawater_correction <- list(as.vector(poly_matrix %*% kgen.pkg.env$poly_coefs[[k]]))
        names(seawater_correction) <- k
      }
    }

    if (k %in% names(seawater_correction)) {
      return(seawater_correction[[k]])
    } else {
      return(1L)
    }
  }
