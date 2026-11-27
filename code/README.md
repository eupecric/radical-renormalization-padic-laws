# Verification programs

Both use Python 3 and the standard library. Original filenames and computational contents are retained.

- `verificar_A2.py`: exact coefficients, valuation checks, finite certificate, truncated ratio system and finite interpolation checks.
- `conferir_kallat_focal_v0_9_1.py`: finite exact-arithmetic checks of the comparison with Kallat.

From the repository root:

```sh
python3 -I -B code/verificar_A2.py
python3 -I -B code/conferir_kallat_focal_v0_9_1.py
```

Run both scripts without arguments. The first uses MB=26, L=10, K=20. It also accepts `26` and `26 10` as explicit defaults for compatibility. Both programs matched the v0.9.3 copies byte for byte and reported `TOTAL FAILURES: 0` in the v0.9.4 validation. See the [verification outputs](../results/README.md) and [reproducibility instructions](../docs/REPRODUCIBILITY.md) for the finite scope of the checks.

## License

The verification programs are distributed under the [MIT License](../LICENSE-MIT), subject to the scope described in [LICENSE.md](../LICENSE.md). The documentation is CC BY 4.0. Keep the license notices when redistributing the programs.
