# Validation report — 2026-10-12
## Verified results
- Backend pytest: **24 passed**, 0 failed.
- Backend Ruff: **all checks passed**.
- Frontend Vitest: **3 passed**, 0 failed.
- TypeScript checking and Vite production build: **passed**.
- Microsoft Edge browser workflows: **2 passed**, 0 failed.
- Windows launcher: start, stop and restart succeeded; the instructional project and completed analysis remained present.

## Coverage
Independent DNA reference: 9 bases, 22.2222% GC, MK*, TCATTTCAT.
Reverse ORF coordinates, RNA handling, alternative code, partial codons, ambiguity denominators, undefined windows, strict validation, multi-FASTA, explicit normalization, nucleotide transformations, protein values, nonstandard residues, invalid codes/start codons and window limits.
API checks: atomic import rejection, duplicate identifiers, analysis completion, CSV/FASTA/JSON/HTML export, source preservation, parent linkage, input hashes, missing resources, invalid titles, foreign origin rejection, cancellation, failure and interrupted-run recovery.
Browser workflows: project creation, paste and actual file import, DNA/RNA/protein results, ORF/translation displays, PNG/SVG/CSV/HTML downloads, theme switching, derived records, reload persistence, invalid symbols, region extraction and parameter recomputation.
Mobile width 390 px: no horizontal page overflow; chart SVG width matches container after resize.
No uncaught browser errors in the primary end-to-end workflow.

## Measured performance
One local synthetic 100,000-base DNA analysis: approximately **0.103 seconds**, 991 full windows (window 1,000, step 100). Measurement covers the scientific function only, not import, database or browser rendering. It is not a genome-scale or worst-case benchmark.
Raw measurement: artifacts/benchmark.json.

## Evidence
- artifacts/e2e-results.json
- artifacts/seq-lab-light.png
- artifacts/seq-lab-dark.png
- artifacts/seq-lab-protein.png
- artifacts/seq-lab-mobile.png
- artifacts/composition.png and composition.svg
- artifacts/browser-composition.csv
- artifacts/browser-report.html

Test databases are isolated in artifacts/test-db and artifacts/e2e-db.
The delivered user database in data/ contains only the clearly labeled instructional example.
The test client emits one upstream Starlette deprecation warning for httpx; tests pass. No workaround or warning suppression was applied.
External scientific integrations and full master-roadmap functionality are not covered because they are not implemented.
