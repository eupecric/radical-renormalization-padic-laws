# Verification programs

Both use Python 3 and the standard library. Original filenames and computational contents are retained.

- `verificar_A2.py`: exact coefficients, valuation checks, finite certificate, truncated ratio system and finite interpolation checks.
- `conferir_kallat_focal_v0_9_1.py`: finite exact-arithmetic checks of the comparison with Kallat.

From the repository root:

```sh
python3 -I -B code/verificar_A2.py
python3 -I -B code/conferir_kallat_focal_v0_9_1.py
```

Use the default configuration (no arguments); the first script uses MB=26, L=10, K=20. Both are expected to report `TOTAL FAILURES: 0`. Historical comments record original development, not release dates. Finite tests are not proofs. See [reproducibility](../docs/REPRODUCIBILITY.md).

## License

The verification programs are distributed under the [MIT License](../LICENSE-MIT), subject to the scope described in [LICENSE.md](../LICENSE.md). The documentation is CC BY 4.0. Keep the license notices when redistributing the programs.
