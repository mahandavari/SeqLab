# Scientific methodology
## Input and normalization
Type selection is explicit because alphabets overlap. DNA supports ACGTRYSWKMBDHVN; RNA replaces T with U. Protein supports the standard residues plus B/X/Z/J/U/O/* for preservation.
The visible normalization option uppercases and removes whitespace. FASTA line wrapping is syntax. Original source text is always retained. Empty records, duplicate identifiers and invalid symbols reject an import.

## Nucleotide calculations
GC = 100(G+C)/(A+C+G+T/U), with ambiguous symbols excluded from the denominator; no canonical symbols means null.
Total-length GC is also stored using every symbol in the denominator. AT uses the canonical denominator. Entropy is -sum(p log2 p) over observed symbols. Dinucleotide counts overlap and retain ambiguity.
Full windows only: start=0,step,2step,... with start+window<=length. Prefix sums keep work linear. GC skew=(G-C)/(G+C); no G/C means null, displayed as a chart gap.

## Coordinates
Internal intervals are zero-based and half-open. UI and CSV are one-based, inclusive. Reverse intervals map [start,end) to [n-end,n-start). Transformations use Biopython and create separate records with parent hash and parameters.

## Translation and ORFs
Six frames use the chosen NCBI genetic code. Trailing partial codons are omitted and counted. Ambiguous codons follow Biopython behavior, including unresolved X. Tables with context-dependent dual-use stops are excluded.
Each frame retains the first configured start after the previous stop. A definite terminal stop is required. Coordinates include the stop; the protein product omits it. Initiation becomes methionine even for an allowed alternative start.
Nested starts, incomplete fragments and circular-origin ORFs are excluded. These predictions are not experimentally validated genes.

## Protein estimates
Biopython ProtParam provides average mass (Da), theoretical pI and charge, aromaticity, instability index and GRAVY. Charge profiles sample pH 0–14 by 0.5.
Hydropathy is the unweighted Kyte–Doolittle moving mean, plotted at window centers. No structural prediction is implied.
Nonstandard residues and stop symbols preserve composition but disable physicochemical calculations; they are not silently removed.

## Reference regression
ATGAAATGA: length 9, two G and zero C, GC 22.2222…%, standard +1 translation MK*, reverse complement TCATTTCAT. The master prompt's former 44.44% was corrected with user approval.

## Sources
- [Biopython sequence reference](https://biopython.org/docs/latest/api/Bio.Seq.html)
- [Biopython ProtParam reference](https://biopython.org/docs/latest/api/Bio.SeqUtils.ProtParam.html)
Installed and verified library: Biopython 1.88. Each result preserves its version and Seq Lab version.
