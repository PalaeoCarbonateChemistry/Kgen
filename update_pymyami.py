"""
Script that updates all resources and version numbers in Python, R and Matlab to ensure that they are in sync.
"""
import urllib.request
from glob import glob
import re

# specify which pymyami version to use throughout Kgen
pymyami_version = '2.1.0'

# path to file containing polynomial coefficients
polynomial_coefficient_path = f'https://raw.githubusercontent.com/PalaeoCarbonateChemistry/pymyami/{pymyami_version}/pymyami/parameters/seawater_correction_approximated.json'

pattern = re.compile(r'(.*)(pymyami==)([0-9.]+)(.*)')

###########################
# Python
###########################

# update requirements.txt
files = ['python/requirements.txt', 'python/pyproject.toml']

for file in files:
    with open(file, 'r+') as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            if pattern.match(line):
                lines[i] = pattern.sub(r'\g<1>\g<2>' + pymyami_version + r'\g<4>', line)
        
        f.seek(0)
        f.write(''.join(lines))
        f.truncate()

###########################
# Matlab
###########################

# update polynomial_coefficients.json

urllib.request.urlretrieve(polynomial_coefficient_path, "matlab/polynomial_coefficients.json")

###########################
# R
###########################

# update polynomial_coefficients.json
urllib.request.urlretrieve(polynomial_coefficient_path, "r/inst/coefficients/polynomial_coefficients.json")

# update pymyami version
with open('r/R/pymyami.R', 'r+') as f:
    lines = f.readlines()
    
    for i, line in enumerate(lines):
        if 'pymyami_version <-' in line:
            lines[i] = f'pymyami_version <- "{pymyami_version}"\n'

    f.seek(0)
    f.write(''.join(lines))
    f.truncate()

# update pymyami version in Github Actions

actions = glob('.github/workflows/*.yml')

for action in actions:
    with open(action, 'r+') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if pattern.match(line):
                lines[i] = pattern.sub(r'\g<1>\g<2>' + pymyami_version + r'\g<4>', line)
        f.seek(0)
        f.write(''.join(lines))
        f.truncate()
