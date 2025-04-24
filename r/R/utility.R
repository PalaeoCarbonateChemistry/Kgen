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
#' @export
calc_pressure_correction <- function(k, temp_c, p_bar) {
  checkmate::assert(
    combine = "and",
    checkmate::check_character(k),
    checkmate::check_numeric(temp_c, lower = 0, upper = 40)
  )

  # Load K_pressure_correction.json
  K_presscorr_coefs <-
    rjson::fromJSON(file = system.file("coefficients/K_pressure_correction.json", package = "kgen"))
  K_presscorr_coefs <- K_presscorr_coefs$coefficients

  out <-
    calc_pc(
      coefficients = K_presscorr_coefs[[k]],
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
#' @param magnesium magnesium concentration in mol/kgsw. If None, modern is assumed (0.0528171). Should be the average magnesium concentration in seawater - a salinity correction is then applied to calculate the magnesium concentration in the sample.
#' @param calcium calcium concentration in mol/kgsw. If None, modern is assumed (0.0102821). Should be the average calcium concentration in seawater - a salinity correction is then applied to calculate the magnesium concentration in the sample.
kgen_poly <-
  function(sal,
           temp_c,
           magnesium = 0.0528171,
           calcium = 0.0102821) {
    temp_k <- temp_c + 273.15

    # Create descriptor vector
    dx <- t(c(temp_k, log(temp_k), sal, magnesium, calcium))

    # Build poly matrix
    dy <- stats::poly(dx, degree = 3, raw = TRUE)

    # Sort by index - according to python output
    out <-
      c(1, dy[order(-attr(dy, "degree"), colnames(dy), decreasing = TRUE)])

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
      poly_coefs <-
        rjson::fromJSON(file = system.file("coefficients/polynomial_coefficients.json", package = "kgen"))
      # Calculate correction factors
      seawater_correction <- NULL
      if (k %in% names(poly_coefs)) {
        seawater_correction <- list(sapply(seq_along(sal), function(ii) {
          poly_coefs[[k]] %*% kgen_poly(
            sal = sal[ii],
            temp_c = temp_c[ii],
            magnesium = magnesium[ii],
            calcium = calcium[ii]
          )
        }, simplify = TRUE))
        names(seawater_correction) <- k
      }
    }

    if (k %in% names(seawater_correction)) {
      return(seawater_correction[[k]])
    } else {
      return(1L)
    }
  }
