#' @title Calculate a single equilibrium constant
#'
#' @description Calculate \strong{a single} specified stoichiometric equilibrium constant at given temperature, salinity, pressure and the concentration of magnesium, calcium, sulphate, and fluorine.
#'
#' @author Dennis Mayk
#'
#' @inheritParams calc_seawater_correction
#' @param p_bar Pressure (Bar) (optional)
#' @param sulphate Sulphate concentration in mol/kgsw. Calculated from salinity if not given.
#' @param fluorine Fluorine concentration in mol/kgsw. Calculated from salinity if not given.
#' @return \strong{A single} K at given conditions
#' @export
calc_K <-
  function(k,
           temp_c = 25,
           sal = 35,
           p_bar = NULL,
           magnesium = 0.0528171,
           calcium = 0.0102821,
           sulphate = NULL,
           fluorine = NULL,
           method = "r_polynomial") {
    # Check input values
    checkmate::assert(
      combine = "and",
      checkmate::check_choice(k, choices = names(K_fns)),
      checkmate::check_choice(
        tolower(method),
        choices = c("r_polynomial", "myami_polynomial", "myami")
      ),
      checkmate::check_string(k),
      checkmate::check_numeric(temp_c, lower = 0, upper = 40),
      checkmate::check_numeric(sal, lower = 30, upper = 40),
      checkmate::check_numeric(magnesium, lower = 0, upper = 0.06),
      checkmate::check_numeric(calcium, lower = 0, upper = 0.06)
    )

    KF <- k_value <- temp_k <- KF_deep <- KF_surf <- KS_deep <- KS_surf <-
    check_pc <- pc <- sws_to_tot_deep <- tot_to_sws_surface <- row_id <- 
    seawater_correction <- NULL
    
    dat <- data.table::data.table(temp_c, sal, p_bar, magnesium, calcium, sulphate, fluorine)
    
    # Celsius to Kelvin
    dat[, temp_k := temp_c + 273.15]

    # Check if miniconda is installed
    if (!mc_exists() & tolower(method) != "r_polynomial") {
      warning("Kgen requires r-Miniconda which appears to not exist on your system.")
      install_confirm <-
        utils::askYesNo("Would you like to install it now?")
      if (install_confirm) {
        install_pymyami()
      } else {
        stop("Closing Kgen.")
      }
    }

    # Load K_calculation.json
    K_coefs <-
      rjson::fromJSON(file = system.file("coefficients/K_calculation.json", package = "kgen"))
    K_coefs <- K_coefs$coefficients

    # Select function and run calculation
    K_fn <- K_fns[[k]]
    dat[, k_value := K_fn(
      coefficients = K_coefs[[k]],
      temp_c = temp_c,
      sal = sal
    )]

    # Pressure correction?
    if (!is.null(p_bar)) {
      # Load K_pressure_correction.json
      K_presscorr_coefs <-
        rjson::fromJSON(file = system.file("coefficients/K_pressure_correction.json", package = "kgen"))
      K_presscorr_coefs <- K_presscorr_coefs$coefficients

      if (is.null(sulphate)) {
        dat[, sulphate := calc_sulphate(sal = sal)]
      } else {
        dat[is.na(sulphate), sulphate := calc_sulphate(sal = sal)]
      }

      if (is.null(fluorine)) {
        dat[, fluorine := calc_fluorine(sal = sal)]
      } else {
        dat[is.na(fluorine), fluorine := calc_fluorine(sal = sal)]
      }

      dat[, KS_surf := K_fns[["KS"]](coefficients = K_coefs[["KS"]],
        temp_c = temp_c,
        sal = sal)]
      dat[, KS_deep := KS_surf * calc_pc(
        coefficients = K_presscorr_coefs[["KS"]],
        p_bar = p_bar,
        temp_c = temp_c
      )]
      dat[, KF_surf := K_fns[["KF"]](coefficients = K_coefs[["KF"]],
        temp_c = temp_c,
        sal = sal)]
      dat[, KF_deep := KF_surf * calc_pc(
        coefficients = K_presscorr_coefs[["KF"]],
        p_bar = p_bar,
        temp_c = temp_c
      )]

      # convert from TOT to SWS before pressure correction
      dat[, tot_to_sws_surface := (1 + sulphate / KS_surf + fluorine / KF_surf) / (1 + sulphate / KS_surf)]

      # convert from SWS to TOT after pressure correction
      dat[, sws_to_tot_deep := (1 + sulphate / KS_deep) / (1 + sulphate / KS_deep + fluorine / KF_deep)]
      dat[, pc := calc_pressure_correction(
        k = k,
        temp_c = temp_c,
        p_bar = p_bar
      )]

      dat[, check_pc := data.table::fifelse(pc != 0, pc, 1)]
      dat[, k_value := k_value * tot_to_sws_surface * check_pc * sws_to_tot_deep]
    }

    dat[, seawater_correction := calc_seawater_correction(
      k = k,
      sal = sal,
      temp_c = temp_c,
      calcium = calcium,
      magnesium = magnesium,
      method = method
    )]

    dat[, k_value := k_value * seawater_correction]

    return(dat$k_value)
  }

#' @title Calculate equilibrium constants for seawater
#'
#' @describeIn calc_K Wrapper to calculate \strong{multiple} stoichiometric equilibrium constants at given temperature, salinity, pressure and the concentration of magnesium, calcium, sulphate, and fluorine.
#'
#' @author Dennis Mayk
#'
#' @inheritParams calc_K
#' @param ks character vectors of Ks to be calculated e.g., c("K0", "K1") (Default: NULL, calculate all Ks)
#' @return Data.table of \strong{multiple} Ks at given conditions
#' @export
calc_Ks <-
  function(ks = NULL,
           temp_c = 25,
           sal = 35,
           p_bar = NULL,
           magnesium = 0.0528171,
           calcium = 0.0102821,
           sulphate = calc_sulphate(sal = sal),
           fluorine = calc_fluorine(sal = sal),
           method = "r_polynomial") {
    # Check if ks is supplied, use K_fns as default
    if (is.null(ks)) {
      ks <- names(K_fns)
    }

    # Calculate ks
    ks_list <- pbapply::pblapply(ks, function(k) {
      calc_K(
        k = k,
        temp_c = temp_c,
        sal = sal,
        p_bar = p_bar,
        magnesium = magnesium,
        calcium = calcium,
        sulphate = sulphate,
        fluorine = fluorine,
        method = method
      )
    })

    # Return data.table
    ks_value <- data.table::data.table(do.call(cbind, ks_list))
    names(ks_value) <- ks

    return(ks_value)
  }