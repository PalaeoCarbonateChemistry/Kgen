## R CMD check results

0 errors | 0 warnings | 0 notes

## Changes in this version (1.1.1)

### Performance
- Vectorized kgen_poly() and calc_seawater_correction() for major performance improvement
- Moved coefficient JSON loading to .onLoad() (eliminates per-call file I/O)

### CRAN compliance
- Moved future/progressr/future.apply from Imports to Suggests with lapply fallback
- Deferred pymyami Python setup to first use (no side-effects at load time)
- Added runnable examples for all exported functions
- Replaced \dontrun{} with \donttest{} for parallel example

### Dependencies
- Updated pymyami dependency to v2.1.3
- Updated reticulate dependency to >= 1.42.0
- Replaced pbapply with optional future.apply for user-controlled parallel backends
- Removed rappdirs and pbapply dependencies
- Removed install_pymyami() (obsolete with reticulate >= 1.42.0)

### Other
- Changed out-of-range input validation from errors to warnings
- Fixed parameter documentation for magnesium/calcium defaults
