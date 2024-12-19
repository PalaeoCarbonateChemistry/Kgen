# Kgen <img src="https://github.com/PalaeoCarb/Kgen/blob/docs/assets/images/logo.png" align="right" alt="" width="120" />
Coefficients for consistently calculating and pressure correcting Ks for carbon calculation. 

### [Find out about Kgen](https://palaeocarbonatechemistry.github.io/Kgen).

## Test Status

Language-specific packages:

[![Check K values - Matlab](https://github.com/PalaeoCarb/Kgen/workflows/Check%20K%20values%20-%20Matlab/badge.svg)](https://github.com/PalaeoCarb/Kgen/actions/workflows/matlab-tests.yml)
[![Check K values - Python](https://github.com/PalaeoCarb/Kgen/workflows/Check%20K%20values%20-%20Python/badge.svg)](https://github.com/PalaeoCarb/Kgen/actions/workflows/python-tests.yml)
[![Check K values - R](https://github.com/PalaeoCarb/Kgen/workflows/Check%20K%20values%20-%20R/badge.svg)](https://github.com/PalaeoCarb/Kgen/actions/workflows/r-tests.yml)

Language inter-comparison:

[![Crosscheck Methods](https://github.com/PalaeoCarb/Kgen/workflows/Crosscheck%20Methods/badge.svg)](https://github.com/PalaeoCarb/Kgen/actions/workflows/crosscheck.yml)

## Development Stuff

### What KGen Does

Kgen will provide K's in a consistent, stable output format from specifically defined inputs that have been checked against external reference values and across platforms. We guarantee to keep the input and output format of Kgen stable within major version number (i.e. within the 'X' of version X.y.z), so that updates will not break [your favourite carbon calculator].

### What Kgen Does Not Do

Kgen is *not* intended to provide Ks in the correct format for [your favourite carbon calculator]. We recommend adding Kgen as an [optional] dependency, and implementing any required input/output parsing within [your favourite carbon calculator].

### Talk to Us!

If you have any ideas for improving Kgen, please [Open a New Issue](https://github.com/PalaeoCarb/Kgen/issues/new/choose) on GitHub to discuss how it might best be implemented.
