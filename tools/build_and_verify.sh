#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
mkdir -p results
rm -f paper/manuscript_A.pdf results/SHA256SUMS
(
  cd paper
  pdflatex -interaction=nonstopmode -halt-on-error manuscript_A.tex
  bibtex manuscript_A
  pdflatex -interaction=nonstopmode -halt-on-error manuscript_A.tex
  pdflatex -interaction=nonstopmode -halt-on-error manuscript_A.tex
) > results/compilation.log 2>&1
test -s paper/manuscript_A.pdf
if grep -E 'LaTeX Warning: (There were undefined references|Citation .* undefined|Reference .* undefined)|Overfull \\[hv]box' paper/manuscript_A.log; then
  echo "Inspect compilation warnings before release." >&2
  exit 1
fi
python3 -I -B code/verificar_A2.py > results/verificar_A2.log 2>&1
python3 -I -B code/conferir_kallat_focal_v0_9_1.py > results/conferir_kallat_focal_v0_9_1.log 2>&1
grep -q 'TOTAL FAILURES: 0' results/verificar_A2.log
grep -q 'TOTAL FAILURES: 0' results/conferir_kallat_focal_v0_9_1.log
if command -v sha256sum >/dev/null 2>&1; then
  hash_cmd=sha256sum
else
  hash_cmd='shasum -a 256'
fi
$hash_cmd README.md CHANGELOG.md CITATION.cff .gitignore LICENSE.md LICENSE-MIT LICENSE-CC-BY-4.0.md \
  paper/manuscript_A.tex paper/references_A.bib paper/manuscript_A.pdf \
  code/README.md code/verificar_A2.py code/conferir_kallat_focal_v0_9_1.py \
  docs/AI_PROVENANCE.md docs/MAIN_RESULTS.md docs/REFERENCES.md docs/REPRODUCIBILITY.md \
  results/README.md results/compilation.log results/verificar_A2.log \
  results/conferir_kallat_focal_v0_9_1.log tools/build_and_verify.sh > results/SHA256SUMS
echo "Build and finite checks completed; visual inspection, final metadata, rights review and approval still required."
