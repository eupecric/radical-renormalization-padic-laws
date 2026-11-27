#!/bin/sh
set -eu
cd "$(dirname "$0")/.."

write_manifest() {
  set -- README.md CHANGELOG.md CITATION.cff .gitignore LICENSE.md LICENSE-MIT LICENSE-CC-BY-4.0.md \
    paper/manuscript_A.tex paper/references_A.bib paper/manuscript_A.pdf \
    code/README.md code/verificar_A2.py code/conferir_kallat_focal_v0_9_1.py \
    docs/AI_PROVENANCE.md docs/MAIN_RESULTS.md docs/REFERENCES.md docs/REPRODUCIBILITY.md \
    results/README.md results/compilation.log results/verificar_A2.log \
    results/conferir_kallat_focal_v0_9_1.log tools/build_and_verify.sh
  if [ -f results/FINAL_RELEASE_VALIDATION.md ]; then
    set -- "$@" results/FINAL_RELEASE_VALIDATION.md
  fi
  manifest_tmp=$(mktemp results/.SHA256SUMS.XXXXXX)
  trap 'rm -f "$manifest_tmp"' EXIT
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$@" > "$manifest_tmp"
  else
    shasum -a 256 "$@" > "$manifest_tmp"
  fi
  mv -f "$manifest_tmp" results/SHA256SUMS
}

if [ "$#" -eq 1 ] && [ "$1" = "--manifest-only" ]; then
  write_manifest
  exit 0
fi
if [ "$#" -ne 0 ]; then
  echo "Usage: sh tools/build_and_verify.sh [--manifest-only]" >&2
  exit 2
fi

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
grep -qx 'TOTAL FAILURES: 0' results/verificar_A2.log
grep -qx 'TOTAL FAILURES: 0' results/conferir_kallat_focal_v0_9_1.log
write_manifest
echo "Build and finite checks completed. SHA-256 manifest written to results/SHA256SUMS."
