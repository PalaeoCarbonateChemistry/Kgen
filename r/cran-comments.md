## 0.3.2
Bump to reticulate 1.42.0 to let uv handle python installation

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

## R CMD check results

0 errors | 0 warnings | 1 note

* This is a new release.
