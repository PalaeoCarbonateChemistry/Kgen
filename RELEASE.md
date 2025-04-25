# Release Checklist for KGen

## Version numbers

Should follow X.Y.Z, where X and Y are cross-platform major and minor releases, and Z can be platform-specific bug fixes.

### Logic

- Performance across all languages will be identical at the X.Y level.
- The .Z level will be used to indicate bug fixes for a specific language, and may therefore differ between languages.

### Major/Minor Update Procedure

1. Make changes to code, commit to GitHub and ensure the test pass verifying agreement between languages.
2. Push a GitHub tag incrementing the appropriate level (i.e. `X.Y+1.0` or `X+1.Y.0`)
3. On GitHub, create a release linked to this tag, and add a description of the changes made. Also add this description to `HISTORY.md`.
4. Follow the instructions below to update the package for the language that has changed.

### Bug Fix Procedure

1. Make changes to code, and push a GitHub Tag incrementing the Z level and identifying the language that was changed, i.e. `X.Y.Z+1 - LANGUAGE`
2. On GitHub, create a release linked to this tag, and add a description of the changes made.
3. Follow the instructions below to update the package for the language that has changed.

## When a new version is released

### Python

- [ ] Update `VERSION` in `kgen/__init__.py`
- [ ] run `make distribute-python`

### matlab

- [ ] Follow the instruction [here](https://www.mathworks.com/help/matlab/matlab_prog/create-and-share-custom-matlab-toolboxes.html)
- [ ] Update the package number
- [ ] Submit to the [Matlab file exchange](https://uk.mathworks.com/matlabcentral/fileexchange/126170-kgen)


### R

- [ ] Update `Version` in `DESCRIPTION`
- [ ] run `devtools::submit_cran()` (must be run by project maintainer only)

## When pymyami is updated 

- [ ] Run `update_pymyami.py` to update all pymyami references to latest version number.
