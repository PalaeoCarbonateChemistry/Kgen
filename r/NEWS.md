# kgen 1.1.1
- Move future/progressr/future.apply to Suggests (CRAN compliance)
- Defer pymyami Python setup to first use (no side-effects at load time)
- Add runnable examples for all exported functions

# kgen 1.1.0
- Vectorized kgen_poly() and calc_seawater_correction() for major performance improvement
- Replaced pbapply with future.apply for user-controlled parallel backends
- Moved coefficient JSON loading to .onLoad() (eliminates per-call file I/O)
- Changed out-of-range input validation from errors to warnings
- Updated pymyami dependency to v2.1.3
- Removed install_pymyami() (obsolete with reticulate >= 1.42.0)
- Removed rappdirs and pbapply dependencies

# kgen 1.0.0
- Stabilise

# kgen 0.4.0
- Updated pymyami dependency to v2.1.1

# kgen 0.3.2
- Bump to reticulate 1.42.0 to let uv handle python installation

# kgen 0.3.0
- Migrated all relevant things to start with 'calc_' instead of 'fn_' (e.g. calc_K1 instead of fn_K1). These are not exported so have no impact on functionality.
- Added wrapper function to calculate seawater correction using Kgen

# kgen 0.2.1
- Initial release
