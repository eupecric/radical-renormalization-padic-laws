# Verification outputs

These files record the local technical validation of the unreleased v0.9.4 manuscript.

- [Compiled PDF](../paper/manuscript_A.pdf)
- [pdfLaTeX and BibTeX compilation log](compilation.log)
- [Exact-arithmetic verifier log](verificar_A2.log)
- [Kallat comparison verifier log](conferir_kallat_focal_v0_9_1.log)
- [Final technical validation report](FINAL_RELEASE_VALIDATION.md)
- [SHA-256 manifest](SHA256SUMS)

Both finite verifiers reported `TOTAL FAILURES: 0`. From the repository root, run `sha256sum -c results/SHA256SUMS` to verify the listed files. The manifest includes the report and omits its own digest. See the [reproducibility instructions](../docs/REPRODUCIBILITY.md) for rebuilding.
