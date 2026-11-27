# Reproducibility

Requirements: Python 3.10 or newer (standard library), pdfLaTeX and BibTeX with amsart, geometry, lmodern, AMS packages, mathtools, mathrsfs, microtype, booktabs, enumitem, xcolor, hyperref and cleveref, POSIX shell and sha256sum or shasum. The previous build used TeX Live 2022 and Python 3.10.12.

Run from the repository root in a clean working copy:

```sh
sh tools/build_and_verify.sh
```

The script compiles the current source to `paper/manuscript_A.pdf`, executes both finite checks and writes fresh logs and a SHA-256 manifest in results/. Inspect the PDF visually, check the final LaTeX log and both Python outputs. Do not copy a historical PDF. A fresh build may produce different bytes across environments. Recompute the manifest after all metadata and license edits, including any new files. The manifest covers the scoped license files; see [licensing](../LICENSE.md). The script is not a proof audit or release authorization. The v0.9.3 build had 22 pages and two zero-failure runs according to its records; v0.9.4 requires its own results.
