import json
import os
import importlib.resources as importlib_resources

coef_path = importlib_resources.files('kgen') / 'coefficients'

with open(os.path.join(coef_path, 'K_calculation.json'), 'r') as f:
    K_coefs = json.load(f)['coefficients']

with open(os.path.join(coef_path, 'K_pressure_correction.json'), 'r') as f:
    K_presscorr_coefs = json.load(f)['coefficients']
