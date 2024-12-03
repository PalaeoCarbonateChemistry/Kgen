"""
Functions for calculating and pressure correcting equilibrium constants using the coefficients in .json files within the 'coefficients' folder.

All functional forms are from Dickson, Sabine and Christian, 2007.

TODO: Think about pH scales!
"""
import numpy as np
from .coefs import K_coefs, K_presscorr_coefs
from pymyami import calculate_seawater_correction, approximate_seawater_correction

def calc_K1K2(coefficients, temp_c, sal):
    """Calculate K1 or K2 from given parameters

    Parameters
    ----------
    coefficients : array-like
        coefficients for K calculation
    temp_c : array-like
        Temperature in Celcius
    sal : array-like
        Salinity

    Returns
    -------
    array-like
        K1 or K2 on XXXXX pH scale.
    """

    temp_k = temp_c+273.15
    return np.power(10, 
        coefficients[0] +
        coefficients[1] / temp_k +
        coefficients[2] * np.log(temp_k) +
        coefficients[3] * sal +
        coefficients[4] * sal * sal
    )
    
def calc_KW(coefficients, temp_c, sal):
    """Calculate KW from given parameters.

    Parameters
    ----------
    coefficients : array-like
        parameters for K calculation
    temp_c : array-like
        Temperature in Celcius
    sal : array-like
        Salinity
        
    Returns
    -------
    array-like
        KW on XXXXX pH scale.
    """

    temp_k = temp_c+273.15
    return np.exp(
        coefficients[0] +
        coefficients[1] / temp_k +
        coefficients[2] * np.log(temp_k) +
        + (coefficients[3] / temp_k + coefficients[4] + coefficients[5] * np.log(temp_k)) * np.sqrt(sal) +
        coefficients[6] * sal
    )
    
def calc_KB(coefficients, temp_c, sal):
    """Calculate KB from given parameters.

    Parameters
    ----------
    coefficients : array-like
        parameters for K calculation
    temp_c : array-like
        Temperature in Celcius
    sal : array-like
        Salinity
        
    Returns
    -------
    array-like
        KB on XXXXX pH scale.
    """

    temp_k = temp_c+273.15
    return np.exp(
        (coefficients[0] + coefficients[1] * np.sqrt(sal) + coefficients[2] * sal) + 
        (
            coefficients[3] +
            coefficients[4] * np.sqrt(sal) +
            coefficients[5] * sal +
            coefficients[6] * sal * np.sqrt(sal) +
            coefficients[7] * sal * sal
        ) / temp_k +
        (coefficients[8] + coefficients[9] * np.sqrt(sal) + coefficients[10] * sal) * np.log(temp_k) +
        coefficients[11] * np.sqrt(sal) * temp_k
    )
    
def calc_K0(coefficients, temp_c, sal):
    """Calculate K0 from given parameters.

    Parameters
    ----------
    coefficients : array-like
        parameters for K calculation
    temp_c : array-like
        Temperature in Celcius
    sal : array-like
        Salinity
            
    Returns
    -------
    array-like
        K0 on XXXXX pH scale.
    """

    temp_k = temp_c+273.15
    return np.exp(
        coefficients[0] +
        coefficients[1] * 100 / temp_k +
        coefficients[2] * np.log(temp_k / 100) +
        sal * (coefficients[3] + coefficients[4] * temp_k / 100 + coefficients[5] * (temp_k / 100) * (temp_k / 100))
    )

def calc_KS(coefficients, temp_c, sal):
    """Calculate KS from given parameters.

    Parameters
    ----------
    coefficients : array-like
        parameters for K calculation
    temp_c : array-like
        Temperature in Celcius
    sal : array-like
        Salinity
            
    Returns
    -------
    array-like
        KS on XXXXX pH scale.
    """
        
    Istr = calc_ionic_strength(sal)
    temp_k = temp_c+273.15
    return np.exp(
        coefficients[0]
        + coefficients[1] / temp_k
        + coefficients[2] * np.log(temp_k)
        + np.sqrt(Istr) * (coefficients[3] / temp_k + coefficients[4] + coefficients[5] * np.log(temp_k))
        + Istr * (coefficients[6] / temp_k + coefficients[7] + coefficients[8] * np.log(temp_k))
        + coefficients[9] / temp_k * Istr * np.sqrt(Istr)
        + coefficients[10] / temp_k * Istr ** 2
        + np.log(1 - 0.001005 * sal)
    )
    
def calc_Ksp(coefficients, temp_c, sal):
    """Calculate Ksp from given parameters

    Parameters
    ----------
    coefficients : array-like
        parameters for K calculation
    temp_c : array-like
        Temperature in Celcius
    sal : array-like
        Salinity

    Returns
    -------
    array-like
        KspA or KspC on XXXXX pH scale.
    """

    temp_k = temp_c+273.15
    return np.power(
        10,
        (
            coefficients[0] + 
            coefficients[1] * temp_k +
            coefficients[2] / temp_k +
            coefficients[3] * np.log10(temp_k) +
            (coefficients[4] + coefficients[5] * temp_k + coefficients[6] / temp_k) * np.sqrt(sal) +
            coefficients[7] * sal +
            coefficients[8] * sal * np.sqrt(sal)
        ),
    )

def calc_KP(coefficients, temp_c, sal):
    """Calculate KP(s) from given parameters
    
    Parameters
    ----------
    coefficients : array-like
        parameters for K calculation
    temp_c : array-like
        Temperature in Celcius
    sal : array-like
        Salinity

    Returns
    -------
    array-like
        KP1, KP2 or KP3 on XXXXX pH scale.
    """

    temp_k = temp_c+273.15
    return np.exp(
        coefficients[0] / temp_k
        + coefficients[1]
        + coefficients[2] * np.log(temp_k)
        + (coefficients[3] / temp_k + coefficients[4]) * np.sqrt(sal)
        + (coefficients[5] / temp_k + coefficients[6]) * sal
    )

def calc_KP3(coefficients, temp_c, sal):
    """Calculate KP3(s) from given parameters
    
    Parameters
    ----------
    coefficients : array-like
        parameters for K calculation
    temp_c : array-like
        Temperature in Celcius
    sal : array-like
        Salinity

    Returns
    -------
    array-like
        KP3 on XXXXX pH scale.
    """

    temp_k = temp_c+273.15
    return np.exp(
        coefficients[0] / temp_k
        + coefficients[1]
        + (coefficients[2] / temp_k + coefficients[3]) * np.sqrt(sal)
        + (coefficients[4] / temp_k + coefficients[5]) * sal
    )

def calc_KSi(coefficients, temp_c, sal):
    """Calculate KSi from given parameters

    Parameters
    ----------
    coefficients : array-like
        parameters for K calculation
    temp_c : array-like
        Temperature in Celcius
    sal : array-like
        Salinity

    Returns
    -------
    array-like
        KSi on XXXXX pH scale.
    """

    Istr = calc_ionic_strength(sal)
    temp_k = temp_c+273.15

    return np.exp(
        coefficients[0] / temp_k + 
        coefficients[1] +
        coefficients[2] * np.log(temp_k) +
        (coefficients[3] / temp_k + coefficients[4]) * Istr ** 0.5 +
        (coefficients[5] / temp_k + coefficients[6]) * Istr +
        (coefficients[7] / temp_k + coefficients[8]) * Istr ** 2
    ) * (1 - 0.001005 * sal)

def calc_KF(coefficients, temp_c, sal):
    """Calculate KSi from given parameters

    Parameters
    ----------
    coefficients : array-like
        parameters for K calculation
    temp_c : array-like
        Temperature in Celcius
    sal : array-like
        Salinity

    Returns
    -------
    array-like
        KF on XXXXX pH scale.
    """
    
    temp_k = temp_c+273.15
    return np.exp(
        coefficients[0] / temp_k + 
        coefficients[1] + 
        coefficients[2] * np.sqrt(sal)
    )

K_fns = {
    "K0": calc_K0,
    "K1": calc_K1K2,
    "K2": calc_K1K2,
    "KW": calc_KW,
    "KB": calc_KB,
    "KS": calc_KS,
    "KspA": calc_Ksp,
    "KspC": calc_Ksp,
    "KP1": calc_KP,
    "KP2": calc_KP,
    "KP3": calc_KP3,
    "KSi": calc_KSi,
    "KF": calc_KF
}    

def calc_pressure_correction(coefficients, p_bar, temp_c):
    """Calculate pressure correction factor for thermodynamic Ks.

    From Millero et al (2007, doi:10.1021/cr0503557)
    Eqns 38-40

    Usage:
    K_corr / K_orig = [output]
    Kcorr = [output] * K_orig

    Parameters
    ----------
    coefficients : array-like
        parameters to calculate pressure correction factors (Kcorr).
    TC : array-like
        Temperature in Celcius
    sal : array-like
        Salinity
    """
    a0, a1, a2, b0, b1 = coefficients
    dV = a0 + a1 * temp_c + a2 * temp_c ** 2
    dk = (b0 + b1 * temp_c)  # NB: there is a factor of 1000 in CO2sys, which has been incorporated into the coefficients for the function.    
    RT = 83.1451 * (temp_c + 273.15)
    return np.exp((-dV + 0.5 * dk * p_bar) * p_bar / RT)    

def calc_seawater_correction(ks, temp_c, sal, magnesium, calcium, MyAMI_mode='calculate'):
    """Calculate seawater correction factor for thermodynamic Ks.

    Wrapper for pymyami functionality

    Parameters
    ----------
    ks : array-like
        list of strings for names of K's
    temp_c : array-like
        Temperature in Celcius
    sal : array-like
        Salinity
    magnesium : array-like
        Magnesium concentration in mol/kg
    calcium : array-like
        Calcium concentration in mol/kg
    MyAMI_mode : str
        Either 'calculate' for full MyAMI or 'approximate' for polynomial approximation
    """
    if MyAMI_mode == 'calculate':
        seawater_correction = calculate_seawater_correction(Sal=sal, TempC=temp_c, Mg=magnesium, Ca=calcium)
    elif MyAMI_mode == 'approximate':
        seawater_correction = approximate_seawater_correction(Sal=sal, TempC=temp_c, Mg=magnesium, Ca=calcium)
    else:
        raise(ValueError("Unknown MyAMI_mode - must be 'calculate' or 'approximate'"))
    
    return {name:seawater_correction[name] for name in ks if name in seawater_correction}

def calc_ionic_strength(sal):
    # Ionic strength after Dickson 1990a; see Dickson et al 2007
    return 19.924 * sal / (1000 - 1.005 * sal)

def calc_sulphate(sal):
    """
    Calculate total Sulphur in mol/kg-SW- lifted directly from CO2SYS.m

    From Dickson et al., 2007, Table 2
    Note: sal / 1.80655 = Chlorinity
    """
    return 0.14 * sal / 1.80655 / 96.062 # mol/kg-SW

def calc_fluorine(sal):
    """
    Calculate total Fluorine in mol/kg-SW

    From Dickson et al., 2007, Table 2
    Note: sal / 1.80655 = Chlorinity
    """
    return 6.7e-5 * sal / 1.80655 / 18.9984 # mol/kg-SW

def calc_K(K, temp_c=25.0, sal=35.0, p_bar=0.0, magnesium=0.0528171, calcium=0.0102821, sulphate=None, fluorine=None, MyAMI_mode='calculate'):
    """
    Calculate a specified stoichiometric equilibrium constant at given
    temperature, salinity and pressure.

    TODO: document pH scales.

    Parameters
    ----------
    k : string
        The name of the K you want to calculate, e.g. 'K1'
    temp_c : array-like
        Temperature in Celcius
    sal : array-like
        Salinity in PSU
    p_bar : array-like
        Pressure in bar
    magnesium : array-like
        magnesium concentration in mol/kgsw. If None, modern is assumed
        (0.0528171). Should be the *average* magnesium concentration in
        seawater - a salinity correction is then applied to calculate
        the magnesium concentration in the sample. Used to correct the Ks
        using MyAMI.
    calcium : array-like
        calcium concentration in mol/kgsw. If None, modern is assumed
        (0.0102821). Should be the *average* calcium concentration in
        seawater - a salinity correction is then applied to calculate
        the magnesium concentration in the sample. Used to correct the Ks
        using MyAMI.
    sulphate : array-like
        Total sulphate in mol/kgsw. Calculated from salinity if not
        given.
    fluorine : array-like
        Total fluorine in mol/kgsw. Calculated from salinity if not
        given.
    MyAMI_mode : str
        Either 'calculate' or 'approximate'. In the former case,
        the full MyAMI model is run to calculate the correction
        factor for the Ks. In the latter, a polynomial function is
        used to approximate the correction factor. The latter is faster,
        though marginally less accurate.

    Returns
    -------
    array-like
        The specified K at the given conditions.
    """
    if K not in K_fns:
        raise ValueError(f'{K} is not valid. Should be one of {K_fns.keys}')

    if temp_c is None:
        temp_c = 25.0
    if sal is None:
        sal = 35.0    
    if p_bar is None:
        p_bar = 0.0

    if fluorine is None:
        fluorine = calc_fluorine(sal=sal)
    if sulphate is None:
        sulphate = calc_sulphate(sal=sal)
        
    K_calc = K_fns[K](coefficients=K_coefs[K], temp_c=temp_c, sal=sal)

    if np.any(p_bar != 0.0):
        KS_surf = K_fns['KS'](coefficients=K_coefs['KS'], temp_c=temp_c, sal=sal)
        KS_deep = KS_surf * calc_pressure_correction(coefficients=K_presscorr_coefs['KS'], p_bar=p_bar, temp_c=temp_c)
        KF_surf = K_fns['KF'](coefficients=K_coefs['KF'], temp_c=temp_c, sal=sal)
        KF_deep = KF_surf * calc_pressure_correction(coefficients=K_presscorr_coefs['KF'], p_bar=p_bar, temp_c=temp_c)
        
        tot_to_sws_surface = (1 + sulphate / KS_surf + fluorine / KF_surf) / (1 + sulphate / KS_surf)  # convert from TOT to SWS before pressure correction
        sws_to_tot_deep = (1 + sulphate / KS_deep) / (1 + sulphate / KS_deep + fluorine / KF_deep)  # convert from SWS to TOT after pressure correction
        
        K_calc *= tot_to_sws_surface * calc_pressure_correction(coefficients=K_presscorr_coefs[K], p_bar=p_bar, temp_c=temp_c) * sws_to_tot_deep

    if np.any(calcium != 0.0102821) or np.any(magnesium != 0.0528171):
        seawater_corrections = calc_seawater_correction(K, temp_c=temp_c, sal=sal, magnesium=magnesium, calcium=calcium, MyAMI_mode=MyAMI_mode)
        if K in seawater_corrections:
            K_calc *= seawater_corrections[K]
    
    return K_calc

def calc_Ks(K_list=K_fns.keys(), temp_c=25.0, sal=35.0, p_bar=0.0, magnesium=0.0528171, calcium=0.0102821, sulphate=None, fluorine=None, MyAMI_mode='calculate'):
    """
    Calculate specified stoichiometric equilibrium constants at given
    temperature, salinity and pressure.

    TODO: document pH scales.

    Parameters
    ----------
    K_list : array-like
        List of Ks to calculate
    temp_c : array-like
        Temperature in Celcius
    sal : array-like
        Salinity in PSU
    p_bar : array-like
        Pressure in bar
    magnesium : array-like
        Magnesium concentration in mol/kgsw. If None, modern is assumed
        (0.0528171). Should be the *average* magnesium concentration in
        seawater - a salinity correction is then applied to calculate
        the magnesium concentration in the sample. Used to correct the Ks
        using MyAMI.
    calcium : array-like
        Calcium concentration in mol/kgsw. If None, modern is assumed
        (0.0102821). Should be the *average* calcium concentration in
        seawater - a salinity correction is then applied to calculate
        the magnesium concentration in the sample. Used to correct the Ks
        using MyAMI.
    sulphate : array-like
        Total sulphate in mol/kgsw. Calculated from salinity if not
        given.
    fluorine : array-like
        Total fluorine in mol/kgsw. Calculated from salinity if not
        given.
    MyAMI_mode : str
        Either 'calculate' or 'approximate'. In the former case,
        the full MyAMI model is run to calculate the correction
        factor for the Ks. In the latter, a polynomial function is
        used to approximate the correction factor. The latter is faster,
        though marginally less accurate.

    Returns
    -------
    dict
        Containing calculated Ks.
    """
    if K_list is None:
        K_list = K_fns.keys()

    if temp_c is None:
        temp_c = 25.0
    if sal is None:
        sal = 35.0    
    if p_bar is None:
        p_bar = 0.0
    
    if fluorine is None:
        fluorine = calc_fluorine(sal=sal)
    if sulphate is None:
        sulphate = calc_sulphate(sal=sal)

    if np.any(calcium != 0.0102821) or np.any(magnesium != 0.0528171):
        seawater_corrections = calc_seawater_correction(K_list, temp_c=temp_c, sal=sal, magnesium=magnesium, calcium=calcium, MyAMI_mode=MyAMI_mode)
    else:
        seawater_corrections = {}

    Ks = {}
    for k in K_list:
        Ks[k] = K_fns[k](coefficients=K_coefs[k], temp_c=temp_c, sal=sal)
        
        if np.any(p_bar != 0.0):
            KS_surf = K_fns['KS'](coefficients=K_coefs['KS'], temp_c=temp_c, sal=sal)
            KS_deep = KS_surf * calc_pressure_correction(coefficients=K_presscorr_coefs['KS'], p_bar=p_bar, temp_c=temp_c)
            KF_surf = K_fns['KF'](coefficients=K_coefs['KF'], temp_c=temp_c, sal=sal)
            KF_deep = KF_surf * calc_pressure_correction(coefficients=K_presscorr_coefs['KF'], p_bar=p_bar, temp_c=temp_c)
            
            tot_to_sws_surface = (1 + sulphate / KS_surf + fluorine / KF_surf) / (1 + sulphate / KS_surf)  # convert from TOT to SWS before pressure correction
            sws_to_tot_deep = (1 + sulphate / KS_deep) / (1 + sulphate / KS_deep + fluorine / KF_deep)  # convert from SWS to TOT after pressure correction

            if k in K_presscorr_coefs:
                Ks[k] *= tot_to_sws_surface * calc_pressure_correction(coefficients=K_presscorr_coefs[k], p_bar=p_bar, temp_c=temp_c) * sws_to_tot_deep                
        
        if k in seawater_corrections:
            Ks[k] *= seawater_corrections[k]            
    
    return Ks