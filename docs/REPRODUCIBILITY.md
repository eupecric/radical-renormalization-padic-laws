# Reproducibility

The build requires Python 3.10 or newer (standard library), pdfLaTeX and BibTeX with amsart, geometry, lmodern, AMS packages, mathtools, mathrsfs, microtype, booktabs, enumitem, xcolor, hyperref and cleveref, a POSIX shell, `mktemp`, and `sha256sum` or `shasum`. The v0.9.4 validation used TeX Live 2022 and Python 3.10.12.

Run from the repository root in a clean working copy:

```sh
sh tools/build_and_verify.sh
```

The script compiles the source to `paper/manuscript_A.pdf`, runs both finite verifiers and writes fresh logs and the SHA-256 manifest in `results/`. A rebuild can produce different bytes, for example because of PDF timestamps and the running times in the logs. The [final validation report](../results/FINAL_RELEASE_VALIDATION.md) describes the specific PDF and logs inspected for v0.9.4.

To regenerate the manifest for the existing artifacts after documentation edits, run the following from the repository root.

```sh
sh tools/build_and_verify.sh --manifest-only
sha256sum -c results/SHA256SUMS
```

Use `shasum -a 256 -c results/SHA256SUMS` where `sha256sum` is unavailable. The manifest covers the license files and includes the validation report when present. Its digest list excludes the manifest itself. See the [licensing scope](../LICENSE.md).
