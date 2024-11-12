import unittest
import os
import pandas as pd
import numpy as np
from glob import glob
import pymyami
import json

RDIFF_TOLERANCE = 0.0001  # tolrate max 0.01% difference
APPROX_TOLERANCE = 0.0041  # tolerance for approximated Ks

def compute_relative_difference(ref, test):
    diff = ref - test
    rdiff = diff / ref
    return rdiff

class crosscheck(unittest.TestCase):
    def test_polynomial_coefficients(self):
        with open('../r/inst/coefficients/polynomial_coefficients.json') as f:
            r_coefs = json.load(f)
            
        with open('../matlab/polynomial_coefficients.json') as f:
            matlab_coefs = json.load(f)
            
        with self.subTest(msg=f'Checking MATLAB polynomial coefficients'):
            for k, ref in pymyami.approximate.SEAWATER_CORRECTION_COEFS.items():
                self.assertIsNone(np.testing.assert_equal(ref, matlab_coefs[k]), msg=f'\nMATLAB polynomial coefficients differ for {k}')
        
        with self.subTest(msg=f'Checking R polynomial coefficients'):
            for k, ref in pymyami.approximate.SEAWATER_CORRECTION_COEFS.items():
                self.assertIsNone(np.testing.assert_equal(ref, r_coefs[k]), msg=f'\nR polynomial coefficients differ for {k}')

    def test_all(self):
        fs = glob('generated_Ks/*.csv')
        
        checks = {}
        langs = set()
        methods = set()
        for f in fs:
            lang, method = os.path.basename(f).replace('.csv', '').split('_')
            langs.add(lang)
            methods.add(method)
            
            if method not in checks:
                checks[method] = {}
            checks[method][lang] = pd.read_csv(f)
        
        # compare approximated to calculated within each language
        approx = checks['approximated']
        calced = checks['calculated']
        for lang in langs:
            test_pass = True
            msg = ''
            
            if lang in approx and lang in calced:
                print(f'Testing {lang} approximated vs. calculated...')

                rdiff = compute_relative_difference(calced[lang], approx[lang])
                             
                maxrdiff = rdiff.abs().max()
                
                if np.all(maxrdiff <= APPROX_TOLERANCE):
                    print(f'    OK')
                else:
                    print(f'    FAIL')
                    msg = f'  Max relative difference:'
                    msg +='\n      ' + maxrdiff[maxrdiff>APPROX_TOLERANCE].to_string().replace('\n', '\n      ')
                    test_pass = False
            
                with self.subTest(msg=f'{lang}: approximated vs. calculated'):
                    self.assertTrue(test_pass, msg=f'\n\nKs outside tolerance ({APPROX_TOLERANCE}):\n{msg}')
                
                
        # make sure the different methods are giving the same result
        for method in checks:
            mlangs = list(checks[method].keys())
            nlangs = len(mlangs)
            if nlangs < 2:
                print(f'Only one language ({lang}) uses {method} method - nothing to compare.')
                continue
            
            print(f'Testing {method} method...')
            for i,j in zip(*np.triu_indices(nlangs, k=1)):
                test_pass = True
                msg = ''
                
                rdiff = compute_relative_difference(checks[method][mlangs[i]], checks[method][mlangs[j]])
                             
                maxrdiff = rdiff.abs().max()
                
                print(f'  {mlangs[i]} vs. {mlangs[j]}')
                if np.all(maxrdiff <= RDIFF_TOLERANCE):
                    print(f'    OK')
                else:
                    print(f'    FAIL')
                    msg = f'  Max relative difference:'
                    msg +='\n      ' + maxrdiff[maxrdiff>RDIFF_TOLERANCE].to_string().replace('\n', '\n      ')
                    test_pass = False
            
                with self.subTest(msg=f'{method}: {mlangs[i]} vs. {mlangs[j]}'):
                    self.assertTrue(test_pass, msg=f'\n\nKs outside tolerance ({RDIFF_TOLERANCE}):\n{msg}')

if __name__ == '__main__':
    unittest.main()
