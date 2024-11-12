import json
import os
import importlib.resources as importlib_resources

# import pkg_resources as pkgrs

with importlib_resources.path('kgen', 'coefficients') as coef_path:

    with open(os.path.join(coef_path, 'K_calculation.json'), 'r') as f:
        K_coefs = json.load(f)['coefficients']

    with open(os.path.join(coef_path, 'K_pressure_correction.json'), 'r') as f:
        K_presscorr_coefs = json.load(f)['coefficients']
