# Seq Lab
Your Sequence. Your Discovery.

## Run
Double-click **Start-SeqLab.cmd** in this folder. The local app opens at http://127.0.0.1:8765.
Dependencies and the production frontend are already prepared on this computer.
To stop the server:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File E:\Projects\SeqLab\Stop-SeqLab.ps1
```
Closing the browser does not stop the server. Do not expose this personal app on the public network.

## First workflow
1. Create a project or choose **Explore an example** (synthetic instructional data).
2. Import raw sequence or FASTA; explicitly select DNA, RNA or Protein.
3. Set analysis parameters, then **Run analysis**.
4. Inspect Overview, Translation, ORFs and Visualizations.
5. Use sequence operations to create a derived copy.
6. Open saved runs from Analysis History.
7. Export FASTA, CSV, JSON, HTML reports or PNG/SVG charts.

For sample-data/intro-dna.fasta use window 3, step 3, minimum ORF 6.
Expected: 9 nt, GC 22.22%, frame +1 MK*, reverse complement TCATTTCAT.

## Delivered release 0.1
React/TypeScript local interface; light/dark themes; projects; FASTA/raw import and explicit validation; sequence pagination and region selection; DNA/RNA composition, GC/GC-skew windows, six-frame translation and complete ORFs; protein properties and profiles; derived records and provenance; background runs and persistent history; real chart exports; CSV/FASTA/JSON and HTML reports.

This is the functional scientific core, not the entire four-release master roadmap.

## Important boundaries
- Only linear sequences; at most 100,000 symbols/record, 100 records/import, 1 MB/import.
- No GenBank/EMBL/FASTQ, alignments, MAFFT, Primer3, RNAfold, restriction maps, BLAST, phylogeny or remote retrieval.
- No annotations, circular maps, native PDF generation, Windows installer, application-wide undo, resizable panels or Persian UI yet.
- No project delete/duplicate or project snapshot re-import. Project JSON is an archival export.
- Reports are HTML; browser Print / Save as PDF is available.
- Cancel prevents committing results; a currently executing bounded computation may finish internally.
- The virtual environment uses the existing base Python runtime on this computer. This directory is not a portable installer.
- Custom CSS and React state replace Tailwind/shadcn/Zustand for this small release. SciPy/pandas are not needed by these calculations.

## Local data
Database: data/seq-lab.sqlite3 (plus WAL/SHM files while running).
Original inputs, derived sequences, parameters, hashes and results persist locally.
Back up the whole data directory after stopping the server.
Logs and test evidence: artifacts/. Dependencies: .venv/ and frontend/node_modules/. Caches: .cache/.
No accounts, telemetry, external fonts, cloud storage or sequence uploads.

## Recreate setup
Requires Python 3.12, Node 22+ (validated with Node 24), and pnpm.
```powershell
Set-Location E:\Projects\SeqLab
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --cache-dir .cache\pip -r backend\requirements.lock.txt
Set-Location frontend
pnpm install --frozen-lockfile --store-dir ..\.cache\pnpm
pnpm run build
Set-Location ..
.\Start-SeqLab.ps1
```
See docs/ENVIRONMENT.md for the existing runtimes used in this build.

## Development and verification
```powershell
Set-Location E:\Projects\SeqLab\backend
..\.venv\Scripts\python.exe -m pytest -q
..\.venv\Scripts\python.exe -m ruff check app tests
Set-Location ..\frontend
pnpm test
pnpm run build
```
For frontend development, start the backend on 8765 and run pnpm dev in frontend.
Browser testing requires Edge and a running server with an isolated SEQ_LAB_DATA folder; run pnpm run test:e2e.
See docs/ARCHITECTURE.md, docs/METHODS.md, docs/VALIDATION.md and docs/ROADMAP.md.
