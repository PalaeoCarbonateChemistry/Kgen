# KGen History.

## 0.3.2
### Python
Bug fix for when temperature/salinity are not specified - default to standard seawater conditions

### R
Small changes for submission to CRAN

## 0.3.1
### All
 - Clean up croscheck workflow and script.
 
### R
- adjust package call in zzz
- initiate `seawater_correction`

### Python
 - Only perform pressure correction if some of the pressures are non-zero.
 - Only perform seawater chemistry correction if some of the Mg and Ca are non-standard.

### Matlab
 - Updates to test scripts to run on pull requests.

## 0.3.0
### All
- Further harmonisation across languages
- Renamed all appropriate functions to start with 'calc_' prefix (e.g. calc_K0, calc_Ks, calc_pressure_correction)
- Moved to using temperature in Celcius (temp_c) as input to *all* functions, rather than sometimes temperature in Kelvin and other times temperature in Celcius

### Python
- All K functions now take three input arguments (coefficients, temp_c, and sal) instead of five (previously: p, temp_k, log(temp_k), sal, and sqrt(sal)).
- prescorr -> calc_pressure_correction
- Added wrapper function to calculate seawater correction using Kgen
- Ionic strength is now in a single function and called where needed (and available to call as needed)
- Docstring improvements/corrections

### R
- Migrated all relevant things to start with 'calc_' instead of 'fn_' (e.g. calc_K1 instead of fn_K1). These are not exported so have no impact on functionality.
- Added wrapper function to calculate seawater correction using Kgen

### Matlab
- Restructed all primary functions to accept keyword arguments - restricting Matlab version to Matlab 2022b and later

## 0.2.0

- Initial release across all languages.
- Harmonised function and parameter names across languages.
- All comparison checks passing.
