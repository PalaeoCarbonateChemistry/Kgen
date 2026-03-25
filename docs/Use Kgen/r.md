---
layout: default
parent: Use Kgen
title: R
permalink: use_kgen/r
---

# R

Documentation to start using Kgen in R.
{: .fs-6 .fw-300 }

[![CRAN status](https://www.r-pkg.org/badges/version/kgen)](https://CRAN.R-project.org/package=kgen)
[![CRANLOGS downloads](https://cranlogs.r-pkg.org/badges/kgen)](https://cran.r-project.org/package=kgen)

## Installation

Kgen is available for installation from CRAN:
`install.packages('kgen')`
or directly from Github using remotes/devtools:
`devtools::install_github('PalaeoCarb/Kgen/r')`

This will install Kgen and its dependencies. Kgen relies on `pymyami` for [Mg] and [Ca] correction factors when using the `MyAMI` or `MyAMI_Polynomial` methods. The required version of `pymyami` is automatically resolved via [reticulate](https://rstudio.github.io/reticulate/) when the package is loaded.

## Getting Started

Four functions are exported:

- `calc_K()` for returning a single K at given conditions
- `calc_Ks()` for returning all available Ks
- `calc_pressure_correction()` for returning a K-specific pressure correction factor
- `calc_seawater_correction()` for returning seawater composition correction factors

```R
library('kgen')

# Calculate a single K
calc_K(k, temp_c, sal, p_bar, magnesium, calcium, sulphate, fluorine, method)

# Calculate multiple Ks
calc_Ks(ks, temp_c, sal, p_bar, magnesium, calcium, sulphate, fluorine, method)

# Pressure correction
calc_pressure_correction(k, temp_c, p_bar)

# Seawater correction
calc_seawater_correction(k, sal, temp_c, magnesium, calcium, method)
```

## Arguments

- **k**: Single K name to calculate, e.g., `"K0"`, `"K1"`.

- **ks**: Character vector of coefficients, i.e., K<sub>0</sub>, K<sub>1</sub>, K<sub>2</sub>, K<sub>W</sub>, K<sub>B</sub>, K<sub>S</sub>, K<sub>spA</sub>, K<sub>spC</sub>, K<sub>P1</sub>, K<sub>P2</sub>, K<sub>P3</sub>, K<sub>Si</sub>, and K<sub>F</sub>. If `NULL` all coefficients will be calculated.

- **temp_c**: Temperature in degree Celsius

- **sal**: Salinity

- **p_bar**: Pressure in bar

- **magnesium**: Magnesium concentration in mol kg<sup>-1</sup>

- **calcium**: Calcium concentration in mol kg<sup>-1</sup>

- **sulphate**: Sulphate concentration in mol/kgsw. Calculated from salinity if not given.

- **fluorine**: Fluorine concentration in mol/kgsw. Calculated from salinity if not given.

- **method**: Options: `R_Polynomial`, `MyAMI_Polynomial`, `MyAMI` (defaults to `"R_Polynomial"`). If set to `MyAMI`, Kgen will calculate Mg and Ca correction factors directly using `pymyami`. If set to `MyAMI_Polynomial`, Kgen will approximate the correction factors using a polynomial approximation in `pymyami`. If set to `R_Polynomial`, Kgen will approximate the correction factors using a built-in polynomial approximation function.

The inputs to **temp_c**, **p_bar**, **sal**, **magnesium**, **calcium**, **sulphate**, and **fluorine** may be single numbers or numeric vectors, but where they are vectors, the length of the vectors must be the same. If any value is not specified, it defaults back to 'standard' conditions of temp_c = 25 °C, sal = 35, and p_bar = 0 bar, with Mg and Ca at modern ocean concentrations (0.0528171 and 0.0102821 mol kg<sup>-1</sup>).

## Parallel Execution

`calc_Ks()` uses the [future](https://future.futureverse.org/) framework for parallel computation. To enable parallel execution, set a `future::plan()` before calling `calc_Ks()`:

```R
library('kgen')

# Enable parallel execution
future::plan(future::multisession, workers = parallel::detectCores() - 1)

# Calculate Ks in parallel
result <- calc_Ks(temp_c = 25, sal = 35)

# Reset to sequential
future::plan(future::sequential)
```

## Details

Kgen installation and operation example:

```R
# Recommended installation through CRAN
> install.packages('kgen')

# Load library
> library('kgen')

# Calculate a single K with default values
> calc_K('K0')
[1] 0.02839188

# Calculate all Ks
> calc_Ks(temp_c = 25, sal = 35)
```

## See also
Refer to [pyMyAMI on PyPi](https://pypi.org/project/pymyami/) to learn how Mg and Ca concentration factors are calculated. Refer to [Reticulate](https://rstudio.github.io/reticulate/index.html) to learn more about how the Python integration in Kgen for R works.
