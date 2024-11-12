import unittest
import json
import os
import numpy as np
from kgen.K_functions import K_fns, calc_pressure_correction, calc_Ks

# boilerplate to deal with file paths
cwd = os.getcwd()

if 'setup.py' in os.listdir(cwd):
    dir = '..'
else:
    dir = '.'

class checkKValues(unittest.TestCase):
    """
    Test calculated Ks against all check values.
    """

    def test_Ks(self):
        with open(dir + "/coefficients/K_calculation.json") as f:
            coefs = json.load(f)

        with open(dir + "/check_values/check_Ks.json") as f:
            check = json.load(f)

        sal = check['input_conditions']['S']
        temp_c = check['input_conditions']['TC']

        for k, p in coefs['coefficients'].items():
            K = K_fns[k](p, temp_c=temp_c, sal=sal)

            check_val = check['check_values'][k]
            sigfig = len(str(check_val).rstrip('0').split('.')[1])  # determine significant figures of check value
            
            self.assertAlmostEqual(np.log(K), check['check_values'][k], msg=f'{k}: {K}', places=sigfig)

    def test_presscorr(self):
        """
        Test pressure correction coefficients on K values.
        """
        with open(dir + '/coefficients/K_pressure_correction.json') as f:
            pcoefs = json.load(f)

        with open(dir + "/check_values/check_presscorr.json") as f:
            check = json.load(f)

        sal = check['input_conditions']['S']
        p_bar = check['input_conditions']['P']
        temp_c = check['input_conditions']['TC']
        
        for k, p in pcoefs['coefficients'].items():
            if k in check['check_values']:            
                pF = calc_pressure_correction(p, p_bar=p_bar, temp_c=temp_c)

                checkval = check['check_values'][k]
            
                self.assertAlmostEqual(pF, checkval, msg=f'{k}: {pF}', places=5)

    def test_boilerplate(self):
        with open(dir + "/check_values/check_Ks.json") as f:
            check = json.load(f)
        S = check['input_conditions']['S']
        TC = check['input_conditions']['TC']

        calc = calc_Ks(temp_c=TC, sal=S)

        for k in calc:
            check_val = check['check_values'][k]
            sigfig = len(str(check_val).rstrip('0').split('.')[1])
            
            self.assertAlmostEqual(np.log(calc[k]), check['check_values'][k], msg=f'{k}: {calc[k]}', places=sigfig)

    def test_calls(self):
        # Tests just to check that function calls work with various possible inputs
        output = calc_Ks() # Empty call (assume everything) 
        output = calc_Ks(temp_c=None,sal=None) # Empty call (assume everything) 
        output = calc_Ks(temp_c=30.0,sal=36.0) # Standard call 
        output = calc_Ks(temp_c=30,sal=36) # Standard call with ints
        output = calc_Ks(temp_c=30.0,sal=36.0,p_bar=2.0) # Standard call plus pressure
        output = calc_Ks(temp_c=30.0,sal=36.0,p_bar=2) # Standard call plus pressure as int
        output = calc_Ks(temp_c=30.0,sal=36.0,p_bar=None) # Standard call plus pressure as None
        output = calc_Ks(temp_c=30.0,sal=36.0,p_bar=2.0,calcium=0.01,magnesium=0.05) # Standard call plus pressure and magnesium and calcium
        output = calc_Ks(temp_c=30.0,sal=36.0,p_bar=2.0,calcium=None,magnesium=None) # Standard call plus pressure and magnesium and calcium as None

        
if __name__ == '__main__':
    unittest.main()