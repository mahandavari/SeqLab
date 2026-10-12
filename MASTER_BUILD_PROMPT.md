# MASTER BUILD PROMPT — SEQ LAB

## 1. Your Role and Mission

Act as an elite multidisciplinary software engineering and computational biology team consisting of:

- Senior Bioinformatics Scientist
- Computational Biologist
- Senior Python Backend Engineer
- Senior React/TypeScript Frontend Engineer
- Scientific Visualization Engineer
- UX/UI Product Designer
- Software Architect
- Quality Assurance and Scientific Validation Engineer

Your mission is to design and build **Seq Lab**, a sophisticated, scientifically trustworthy, visually polished, extensible bioinformatics sequence analysis application.

**Product name:** Seq Lab  
**Tagline:** Your Sequence. Your Discovery.

Seq Lab should feel like a modern scientific research environment rather than a collection of unrelated calculators.

The product must enable scientists, students, and researchers to import biological sequences, explore them interactively, perform authentic computational analyses, compare sequences, visualize results, manage research projects, and export publication-quality outputs.

Build a working application with real algorithms, persistent data, integrated workflows, reliable error handling, and a professional user experience.

Do not deliver a static mockup, decorative dashboard, or collection of nonfunctional buttons.

Use an iterative development process, delivering a fully operational core before expanding into advanced modules.

---

## 2. Product Vision

Create a comprehensive, modular **Bioinformatics Workbench** combining five essential capabilities:

1. **Sequence Management:** Importing, editing, validating, annotating, organizing, and exporting biological sequences.
2. **Scientific Analysis:** Performing genuine DNA, RNA, protein, and comparative sequence analyses.
3. **Scientific Visualization:** Generating accurate interactive charts, sequence maps, alignments, and analytical figures.
4. **Research Workflows:** Connecting analysis tools into reproducible workflows and preserving results.
5. **Research Reporting:** Producing clear, traceable, reproducible, publication-ready reports.

Benchmark relevant functionality against mature research software such as UGENE and Benchling, while creating an original design, architecture, and implementation.

Do not attempt to reproduce every advanced feature immediately.

Distinguish clearly between foundational capabilities, advanced analytical modules, and future research-grade extensions.

---

## 3. Target Platform and Technology Stack

Prioritize a Windows-compatible, desktop-first, local-first architecture.

### Frontend
- React
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui
- Lucide Icons
- Plotly.js for interactive scientific charts
- D3.js or other specialized libraries only where appropriate
- Zustand or similarly lightweight state management

### Scientific Backend
- Python
- FastAPI
- Biopython
- NumPy
- SciPy
- pandas
- Appropriate validated scientific packages as needed

### Persistence
- SQLite for local projects and metadata
- SQLModel or SQLAlchemy
- Filesystem-based storage for large sequence datasets
- Versioned project manifests and analysis records

### External Scientific Engines
Integrate established software rather than reimplementing complex validated algorithms unnecessarily:

- MAFFT for multiple sequence alignment
- Primer3 for primer design
- BLAST+ for local sequence similarity searching
- NCBI BLAST API for optional remote searching
- ViennaRNA for RNA secondary structure prediction
- Other scientific engines only when supported by reliable documentation and compatible licensing

### Desktop Packaging
Begin with a locally hosted application using React and FastAPI.

Once the working application is stable, package it as a desktop application using Tauri with a properly managed Python backend sidecar, or another justified packaging architecture.

Do not prematurely introduce packaging complexity.

The initial production target is Windows, with a clean path toward macOS and Linux.

The scientific backend must be independent of the interface, enabling future web and desktop variants.

Verify dependency compatibility with the installed Python version before finalizing the stack.

Do not require a GPU for basic sequence analysis.

---

## 4. Design Philosophy and Visual Identity

Seq Lab should look like a premium scientific software product.

### Design Direction

Combine:
- Modern research laboratory aesthetics
- Clean scientific dashboards
- Professional analytical software
- Minimalism and information density
- Elegant typography
- Precise scientific visualizations

Avoid:
- Generic chatbot-style interfaces
- Oversized decorative elements
- Excessive gradients and animations
- Unnecessary glassmorphism
- Crowded scientific panels
- Fake terminal outputs
- Charts containing placeholder data

### Theme

Implement polished light and dark themes.

Suggested visual language:
- Deep navy and charcoal surfaces
- Off-white light mode backgrounds
- Cyan and teal analytical accents
- Restrained purple for specialized modules
- Consistent semantic colors
- Subtle borders and shadows

Biological sequence colors must remain distinguishable and accessible in both themes.

### Core Layout

Design a professional workspace with:

**Left Sidebar**
- Dashboard
- Sequence Studio
- DNA Analysis
- RNA Analysis
- Protein Analysis
- Visualization Lab
- Alignment Lab
- Evolution Lab
- Molecular Tools
- Projects
- Reports
- Settings

**Top Toolbar**
- Active project
- Active sequence
- Search
- Import
- Export
- Save
- Run analysis
- Processing status

**Main Workspace**
- Resizable panels
- Tabbed documents
- Sequence editor
- Interactive plots
- Results tables
- Optional split-screen comparison

**Right Inspector**
- Selected sequence metadata
- Selected region properties
- Analysis parameters
- Feature annotations
- Scientific explanations
- Context-sensitive actions

Build a responsive interface, but prioritize the desktop research workflow.

Provide keyboard shortcuts, tooltips, searchable commands, undo/redo, loading states, empty states, and actionable error messages.

Use English as the default scientific interface language. Architect localization support for future Persian translations, including correct RTL behavior.

---

# 5. Sequence Input and Management

Implement a robust sequence import system.

### Supported Input Methods

- Direct sequence paste
- FASTA text paste
- Drag-and-drop file upload
- File selection
- Multi-record FASTA files
- GenBank files
- EMBL files when supported
- FASTQ files in the appropriate quality analysis workflow
- Optional retrieval from NCBI using accession identifiers

### Sequence Types

Support:
- DNA
- RNA
- Protein

Automatically suggest sequence type while allowing explicit user selection.

If a sequence is ambiguous, request clarification rather than making an unjustified assumption.

### Input Validation

Validate sequences against appropriate IUPAC alphabets.

Detect and report:
- Invalid characters
- Duplicate sequence identifiers
- Empty records
- Inconsistent sequence types
- Unexpected sequence formatting
- Missing FASTQ quality scores
- Malformed records
- Unsupported file types

Preserve original sequence records and identifiers.

Do not silently change ambiguous bases, remove biologically meaningful characters, or convert RNA to DNA without communicating the operation.

Provide explicit normalization options.

### Sequence Viewer

Build an interactive biological sequence viewer with:

- Position numbering
- Configurable line wrapping
- Monospaced sequence display
- Biological character coloring
- Region selection
- Zooming and navigation
- Forward and reverse strands
- Complement view
- Reading frame visualization
- Annotation tracks
- Motif highlighting
- Feature searching
- Copy selected region
- Export selected region

Display precise start/end coordinates and sequence lengths.

Use an internally consistent zero-based, half-open coordinate representation and a clearly documented one-based, inclusive user-facing representation.

Correctly handle reverse-strand annotations and circular sequences.

For large sequences, implement virtualization or chunked rendering rather than placing the entire sequence into the DOM.

---

# 6. DNA Analysis Module

Build a complete DNA analysis environment.

### Basic Statistics

Calculate:
- Sequence length
- A, T, G, C counts
- Nucleotide frequencies
- GC percentage
- AT percentage
- Ambiguous nucleotide counts
- Dinucleotide frequencies
- K-mer frequencies
- Sequence entropy
- CpG observed/expected ratio where meaningful

Explicitly document how ambiguous bases affect denominators and calculations.

### Sequence Operations

Support:
- Reverse
- Complement
- Reverse complement
- DNA to RNA transcription
- RNA to DNA conversion
- Subsequence extraction
- Sequence joining
- Motif search
- Pattern highlighting
- FASTA formatting
- Coordinate-preserving sequence transformations

### ORF Finder

Implement open reading frame identification using configurable parameters:

- All six reading frames
- Minimum ORF length
- Configurable initiation codons
- Selected genetic code
- Stop codon identification
- ORF coordinates
- Strand orientation
- Predicted translated product

Visualize ORFs along the nucleotide sequence.

Distinguish ORF detection from experimentally validated gene identification.

### Translation

Implement:
- Six-frame translation
- Selectable NCBI genetic code
- Reading frame selection
- Stop codon visualization
- Partial codon handling
- Ambiguous codon handling
- DNA/RNA/protein coordinated display

### Motif and Pattern Search

Include:
- Exact sequence search
- IUPAC-aware motif search
- Configurable mismatch search where supported
- Reverse strand search
- Overlapping matches
- Optional regular expression search with safe execution limits

Show match coordinates and highlighting.

---

# 7. RNA Analysis Module

Provide standard RNA sequence analysis:

- RNA nucleotide composition
- GC content
- RNA motif detection
- Open reading frame analysis where applicable
- Translation
- RNA sequence transformations

### RNA Secondary Structure

Integrate ViennaRNA / RNAfold as an optional installed scientific engine.

Support:
- Minimum free energy structure prediction
- Dot-bracket notation
- MFE value and units
- Secondary structure visualization
- Base-pairing information
- Temperature and relevant model parameters
- Optional base-pair probability visualization

Clearly explain the difference between predicted secondary structures and experimentally verified structures.

Do not generate artificial folding results when ViennaRNA is unavailable.

If the dependency is missing, provide installation guidance and mark the feature unavailable.

---

# 8. Protein Analysis Module

Create a dedicated protein characterization workspace.

### Primary Sequence Analysis

Calculate:
- Amino acid composition
- Sequence length
- Approximate molecular weight
- Theoretical isoelectric point
- Estimated charge at selected pH
- Aromaticity
- Instability index
- GRAVY
- Hydropathy profiles
- Selected physicochemical properties

Use well-documented scientific methods, including Biopython ProtParam where appropriate.

Clearly label theoretical, estimated, and empirical values.

### Protein Visualization

Implement:
- Amino acid frequency chart
- Hydropathy plot
- Charge versus pH graph
- Residue property profiles
- Sequence feature tracks
- Interactive region selection

### Advanced Extensions

Architect optional integrations for:
- Conserved motif/domain searching
- UniProt annotations
- Known protein structure retrieval
- PDB structure visualization
- Validated secondary structure prediction tools

Do not imply that simple sequence heuristics provide reliable tertiary structure predictions.

---

# 9. Visualization Lab

Scientific visualization is one of the defining features of Seq Lab.

Build a centralized visualization environment capable of displaying and exporting real computational results.

### Required Charts

**DNA and RNA**
- Nucleotide composition bar chart
- Base frequency donut or pie chart
- GC content sliding-window plot
- GC skew sliding-window plot
- Dinucleotide frequency heatmap
- K-mer distribution chart
- Codon usage frequency chart
- ORF map
- Sequence feature map
- Interactive restriction map

**Protein**
- Amino acid composition chart
- Hydropathy plot
- Charge versus pH chart
- Protein property profiles

**Comparative Analysis**
- Sequence identity charts
- Alignment conservation profiles
- Pairwise similarity heatmaps
- Dot plots
- Phylogenetic tree viewer

**FASTQ Quality**
- Per-position quality distribution
- Per-read mean quality
- Read length distribution
- GC distribution
- Ambiguous base frequency

### Interactive Features

Charts must support:
- Zoom
- Pan
- Hover values
- Region selection
- Series toggling
- Configurable color palettes
- Configurable window size and step
- Accurate legends
- Axis labels and units
- Method descriptions
- Export to PNG
- Export to SVG where technically supported
- Export underlying data as CSV/TSV

Where practical, selecting a region in a graph should highlight the corresponding nucleotides or residues in the sequence viewer.

Whenever an analysis parameter changes, results should be recalculated rather than visually modified without scientific recomputation.

All graphs must use actual outputs from real algorithms.

Provide clearly labeled example datasets when demonstrating functionality.

---

# 10. Sequence Alignment Lab

Implement scientifically valid pairwise and multiple sequence alignment capabilities.

### Pairwise Alignment

Provide:
- Global alignment
- Local alignment
- Configurable scoring
- Gap opening penalties
- Gap extension penalties
- Nucleotide/protein scoring configurations
- Identity percentage
- Alignment length
- Mismatches
- Gap counts
- Alignment score

Clearly distinguish alignment scores from biological percentage identity.

### Multiple Sequence Alignment

Integrate MAFFT as an external scientific engine.

Features:
- Multiple FASTA input
- Alignment configuration
- Progress tracking
- Alignment viewer
- Position numbering
- Consensus visualization
- Conservation highlighting
- Column-based statistics
- Export aligned FASTA
- Export supported alignment formats

Validate input sequences before execution.

Provide clear explanations when sequences are incompatible or an external engine is unavailable.

### Comparison Tools

Provide:
- Side-by-side sequence comparison
- Difference highlighting
- Pairwise identity matrix
- Sequence dot plots
- Interactive mismatch navigation

Do not implement sophisticated aligners using simplistic or scientifically invalid substitute algorithms.

---

# 11. Evolution and Phylogeny Lab

Provide phylogenetic analysis based on genuine aligned sequence data.

Initial supported workflow:

1. Import compatible sequences.
2. Perform multiple sequence alignment.
3. Inspect and optionally trim alignment.
4. Select a supported phylogenetic method.
5. Construct a tree using a validated implementation.
6. Visualize and export the result.

Start with an accurately implemented distance-based approach such as Neighbor Joining.

Support:
- Branch lengths where defined
- Sequence labels
- Tree rerooting where appropriate
- Newick export
- Basic tree visualization
- Scientific method metadata

More advanced methods and bootstrap support should be added only when correctly implemented.

Never invent branch confidence values.

Explain that phylogenetic inference depends on alignment quality, evolutionary models, and chosen methods.

---

# 12. Molecular Biology Tools

Implement additional tools as independently testable modules.

### Primer Design

Integrate Primer3.

Allow configuration of:
- Primer length
- GC percentage
- Melting temperature
- Product size
- Primer pairing constraints
- Sequence target region
- Hairpin/dimer considerations

Display primer candidates, sequences, positions, strand orientations, thermodynamic metrics, and design constraints.

Make primer specificity checking a separate validated operation rather than assuming all candidate primers are specific.

### Restriction Enzyme Analysis

Provide:
- Recognition site identification
- Cut coordinates
- Restriction enzyme selection
- Linear sequence maps
- Circular plasmid maps
- Fragment-length calculation
- Selected-enzyme comparison

Use validated enzyme recognition definitions.

### Additional Tools

Plan support for:
- In silico PCR
- Restriction digest simulation
- Sequence repeat detection
- CpG region exploration
- Codon usage comparison
- Sequence complexity analysis

Advanced CRISPR guide design may be a future module, provided it uses validated specificity and off-target methods.

---

# 13. Online Biological Database Integration

Build an optional online research integration layer.

Start with:
- NCBI sequence retrieval
- Accession lookup
- Metadata retrieval
- NCBI BLAST

Future integrations may include:
- UniProt
- Ensembl
- PDB
- Other public biological resources

Requirements:
- Respect official API policies
- Implement appropriate rate limits
- Cache results where allowed
- Handle timeouts and unavailable services
- Use retry strategies with safe backoff
- Track accession identifiers and versions
- Identify database source and retrieval time
- Clearly distinguish online and offline operations

Remote BLAST results must come from actual BLAST execution.

Never simulate database hits.

The application's main analysis capabilities must remain operational offline.

---

# 14. Project Management and Research Workspaces

Users must be able to create persistent research projects.

Each project should contain:
- Project identifier and title
- Description
- Imported sequence datasets
- Sequence metadata
- User-created annotations
- Analysis runs
- Parameters
- Results
- Figures
- Exported reports
- Creation and modification timestamps

Provide:
- Project creation
- Rename
- Duplicate
- Save
- Open
- Delete
- Import/export project bundles
- Recent projects
- Search and filtering

Preserve original imported data.

Store analysis outputs separately from source records.

Track transformations and edits so results remain traceable.

Introduce a structured scientific analysis run model with input identifiers, input hashes, algorithm name, tool version, parameters, output artifacts, status, and timestamps.

Use content hashing where appropriate to support result integrity and caching.

---

# 15. Workflow Engine

Create a modular analysis execution architecture.

Each analysis should behave like an independent unit with:

- Unique identifier
- Supported sequence types
- Input schema
- Parameter schema
- Validation rules
- Execution function or engine adapter
- Structured output schema
- Error handling
- Test coverage
- Scientific method metadata

Examples of workflows:

**DNA Characterization**
Import → Validate → Compute Composition → Sliding Window Analysis → Visualize → Export

**Protein Characterization**
Import → Validate → Compute Physicochemical Properties → Visualize → Export

**Comparative Genomics**
Import Multiple Sequences → Validate → Align → Calculate Conservation → Compare → Export

**Phylogenetics**
Import → Multiple Alignment → Distance Calculation → Tree Construction → Visualization → Export

Long-running operations must support background execution, progress reporting, cancellation, and clear failure states.

Avoid blocking the main UI thread.

---

# 16. Scientific Accuracy and Reproducibility

Scientific validity is non-negotiable.

Implement the following principles:

1. Every analytical result must originate from actual input data.
2. Every calculation must follow a defined and documented method.
3. Never invent numerical results, database matches, confidence values, or annotations.
4. Never confuse biological predictions with experimentally verified observations.
5. Show important scientific assumptions.
6. Preserve analysis parameters.
7. Record relevant dependency and tool versions.
8. Handle incomplete or ambiguous biological sequences explicitly.
9. Clearly label unsupported analyses.
10. Ensure graphical outputs correspond to actual computed values.
11. Preserve data provenance.
12. Use standard biological conventions for sequences and coordinates.

Important scientific edge cases include:

- Empty sequences
- Ambiguous nucleotides
- Mixed DNA/RNA inputs
- Protein sequences containing stop symbols
- Partial codons
- Alternative genetic codes
- Short sequences
- Circular sequences
- Reverse-strand features
- Missing annotations
- Invalid alignment input
- Very large files

Gene, promoter, coding region, and regulatory element claims must not be generated from raw sequence data unless supported by a defined analytical method or external annotation source.

---

# 17. Scientific Testing and Validation

Build a serious automated test suite.

Use pytest for backend tests and suitable frontend testing tools.

### Unit Testing

Test:
- Sequence parsers
- Sequence validation
- Coordinate transformations
- Reverse complement
- Transcription
- Translation
- Nucleotide composition
- GC calculation
- Sliding-window calculations
- ORF detection
- Protein property calculations
- Result serialization

### Known Reference Example

For the DNA sequence:

`ATGAAATGA`

Using the standard genetic code:

- Sequence length: 9 nucleotides
- GC content: approximately 22.22% (2 G/C nucleotides out of 9)
- Forward translation in frame +1: `MK*`
- Reverse complement: `TCATTTCAT`

Use this as one introductory regression test alongside more comprehensive scientific test cases.

### Integration Testing

Test:
- FASTA import to DNA analysis
- FASTA import to protein analysis
- Alignment workflows
- Primer3 execution when installed
- MAFFT execution when installed
- Project saving and reopening
- Figure export
- Report generation

### Scientific Benchmark Testing

Compare numerical outputs against:
- Biopython reference behavior
- Established scientific tools
- Published algorithm definitions
- Small independently verified example datasets

Do not treat agreement between two copies of the same faulty implementation as independent validation.

### Quality Requirements

Implement:
- Structured logging
- Type checking
- Linting
- Frontend component tests
- API tests
- Scientific regression tests
- Error-boundary handling
- End-to-end workflow tests

Prioritize real functionality and scientific correctness over superficial coverage metrics.

---

# 18. Performance Engineering

Optimize for a typical personal research computer.

Baseline target:
- Windows laptop
- 16 GB RAM
- Modern multi-core CPU
- Optional NVIDIA GPU

Basic analytical workflows must run without GPU acceleration.

Use:
- Efficient sequence parsing
- Streaming for large inputs where appropriate
- Incremental processing
- Virtualized sequence rendering
- Cached analysis results
- Efficient computation
- Asynchronous processing for heavy jobs

Avoid loading entire very large FASTA or FASTQ collections into memory unnecessarily.

Introduce sensible dataset and job size limits with informative messages.

Measure and document actual performance rather than claiming support for untested genome-scale workloads.

---

# 19. Data Security and Privacy

Seq Lab should be local-first.

Default behavior:
- Local data processing
- Local project persistence
- No account required
- No mandatory cloud synchronization
- No unrequested sequence uploads
- No mandatory analytics or telemetry

External biological database queries must be clearly identified as network operations.

Protect:
- API credentials
- Local project files
- Temporary files
- User paths
- Imported datasets

Never store secrets in frontend source code.

Validate file paths and uploads.

External command-line scientific tools must be invoked safely without shell injection vulnerabilities.

Provide clear data deletion and temporary-file cleanup behavior.

---

# 20. Research Reports and Scientific Export

Create a professional Report Builder.

Reports should include:
- Project title
- Analysis date
- Sequence identifiers
- Sequence metadata
- Analysis objective
- Methods
- Parameters
- Scientific results
- Tables
- Figures
- Limitations
- Software and dependency versions

Support:
- PDF export
- HTML export
- CSV/TSV tables
- FASTA output
- PNG figures
- SVG figures when supported
- Newick tree output where applicable
- Machine-readable analysis metadata

Allow users to select which analyses and figures appear in reports.

Use clean scientific figure captions, accurate labels, appropriate units, and reproducible analysis descriptions.

Do not fabricate research conclusions.

---

# 21. Architecture and Code Quality

Organize the project into a maintainable monorepo structure resembling:

seq-lab/
- frontend/
- backend/
- backend/app/api/
- backend/app/core/
- backend/app/models/
- backend/app/schemas/
- backend/app/services/
- backend/app/scientific/
- backend/app/integrations/
- backend/app/workflows/
- backend/tests/
- desktop/
- docs/
- sample-data/
- scripts/

Refine this structure according to real implementation requirements.

Enforce:
- Clear separation of concerns
- Reusable React components
- Typed API contracts
- Modular scientific algorithms
- Proper exception handling
- Structured data models
- Dependency isolation
- Maintainable documentation
- Consistent naming conventions

Avoid monolithic application files.

Avoid unnecessary framework complexity.

Use established scientific libraries instead of writing custom replacements for mature algorithms without justification.

---

# 22. Development Roadmap

Implement Seq Lab through four progressive releases.

## Phase 1 — Functional Scientific Core

Build a polished working MVP containing:

- Application shell and navigation
- Light and dark mode
- Project creation and local persistence
- Sequence paste and FASTA import
- DNA/RNA/protein validation
- Sequence viewer
- Nucleotide composition
- GC analysis
- Reverse complement
- Translation
- Basic ORF finder
- Protein primary sequence analysis
- Interactive scientific plots
- Chart export
- Analysis history
- Automated tests

This phase must be a complete and demonstrable working application.

## Phase 2 — Comparative Bioinformatics

Add:
- Pairwise alignment
- Multiple sequence alignment with MAFFT
- Alignment visualization
- Comparison statistics
- Dot plots
- FASTQ quality analysis
- Advanced sequence maps
- Report generation

## Phase 3 — Advanced Molecular Tools

Add:
- Primer3 integration
- Restriction analysis
- In silico PCR
- RNAfold integration
- Phylogenetic analysis
- NCBI sequence retrieval
- BLAST integration

## Phase 4 — Desktop Production Release

Add:
- Windows desktop packaging
- First-run installation validation
- Reliable scientific dependency distribution
- Improved large-sequence performance
- Integrated help and documentation
- Scientific validation report
- Comprehensive end-to-end testing
- Release packaging and versioning
- Installer and uninstall process

Optional future research modules should be separately planned rather than silently added to the initial scope.

---

# 23. User Experience Requirements

A new user should be able to:

1. Launch Seq Lab.
2. Create a research project.
3. Paste or import a DNA sequence.
4. See immediate validated sequence statistics.
5. Generate a GC content visualization.
6. Identify ORFs.
7. Translate the sequence.
8. Explore linked analytical visualizations.
9. Save the project.
10. Export scientific results.
11. Close and reopen the application without losing work.

The experience must be intuitive without sacrificing advanced scientific functionality.

Every analytical tool should provide a compact explanation of its scientific purpose, input requirements, parameters, and interpretation limits.

Provide sample projects demonstrating the software's capabilities with clearly identified real or instructional sequence data.

---

# 24. Acceptance Criteria

Do not mark a module complete unless:

- Its interface exists.
- Its backend implementation exists.
- Its inputs are validated.
- Its actual algorithm executes.
- Its outputs are visible.
- Its numerical results are verified.
- Its errors are handled.
- Its tests pass.
- It integrates with the existing application.
- It is documented.

Buttons that do nothing are unacceptable.

Fake scientific charts are unacceptable.

Placeholder analysis results are unacceptable.

A successful implementation requires a functional vertical workflow from raw sequence input to actual result visualization.

---

# 25. Execution Instructions for the Coding Agent

Start by examining the development environment and identifying available tools and dependencies.

Then:

**Step 1 — Architecture and Product Definition**

Produce:
- Concise product requirements
- Module dependency map
- Recommended implementation architecture
- Database schema proposal
- Scientific validation strategy
- Practical phased development plan

Explain major technical trade-offs, especially desktop packaging and external scientific tools.

**Step 2 — Repository Setup**

Create the actual project structure.

Initialize the frontend, backend, environment configuration, dependency manifests, documentation, and testing tools.

Provide Windows PowerShell-compatible instructions.

**Step 3 — Implement the First Vertical Slice**

Create a fully functional workflow:

Sequence Import → Sequence Validation → Real DNA Analysis → Interactive Visualization → Save Results → Export.

This workflow must work end to end before starting less essential functionality.

**Step 4 — Expand the Scientific Core**

Implement the remaining Phase 1 modules with tests and integrated interfaces.

**Step 5 — Build Subsequent Modules**

Follow the planned development phases.

Prioritize validated scientific tools, stable interfaces, and maintainability.

**Step 6 — Verification**

Run available tests, inspect application behavior, fix actual failures, and document unresolved issues.

Do not claim successful tests or execution that did not occur.

**Step 7 — Delivery**

Provide:
- Working application source code
- Installation instructions
- Development commands
- Production execution guidance
- Test results
- Architecture documentation
- Scientific methodology documentation
- List of implemented capabilities
- Honest list of incomplete capabilities
- Instructions for adding future modules

### Important Working Rules

- Work directly in the project repository when filesystem tools are available.
- Prefer implementing and verifying working files rather than dumping enormous amounts of disconnected code into chat.
- Make reasonable engineering decisions without repeatedly requesting confirmation.
- Ask questions only when a missing requirement genuinely blocks implementation.
- Never silently substitute simulations for real scientific algorithms.
- Never present an unavailable external integration as operational.
- If a dependency requires installation or licensing review, document it explicitly.
- Keep the application operational after each development phase.
- If execution is interrupted, clearly report the last verified working state and the next unfinished task.
- Treat scientific accuracy, user experience, performance, and maintainability as equally important engineering concerns.

## Final Goal

The final application should look and behave like a credible professional bioinformatics research environment.

It must be useful to biology students, molecular biologists, computational biologists, and researchers.

Its core identity should be:

**SEQ LAB — A powerful, accessible, scientifically trustworthy environment for biological sequence exploration, analysis, and visualization.**

Begin with the architecture and Phase 1 implementation. Prioritize a working, scientifically validated product over an impressive but superficial demonstration.