from collections import Counter
from math import log2
from Bio import __version__ as bio_version
from Bio.Data import CodonTable
from Bio.Seq import Seq
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from Bio.SeqUtils.ProtParamData import kd

def genetic_codes():
    return [{"id": key, "name": table.names[0], "starts": table.start_codons}
            for key, table in sorted(CodonTable.unambiguous_dna_by_id.items())
            if not (set(table.stop_codons) & set(table.forward_table))]

def windows(sequence, size, step):
    if size > len(sequence):
        return []
    count = (len(sequence) - size) // step + 1
    if count > 10_000:
        raise ValueError("More than 10,000 windows. Increase the step size.")
    # Prefix counts keep sliding-window calculations linear in sequence length.
    prefixes = {b: [0] for b in "ACGTU"}
    for char in sequence:
        for b, values in prefixes.items():
            values.append(values[-1] + (char == b))
    rows = []
    for start in range(0, len(sequence) - size + 1, step):
        end = start + size
        counts = {b: values[end] - values[start] for b, values in prefixes.items()}
        gc = counts["G"] + counts["C"]
        canonical = sum(counts.values())
        rows.append({"start": start, "end": end, "gc": 100 * gc / canonical if canonical else None,
                     "skew": (counts["G"] - counts["C"]) / gc if gc else None,
                     "canonical": canonical})
    return rows

def find_orfs(dna, table, min_nt, starts):
    n, found = len(dna), []
    for strand, oriented in [(1, dna), (-1, str(Seq(dna).reverse_complement()))]:
        for offset in range(3):
            begin = None
            for pos in range(offset, n - 2, 3):
                codon = oriented[pos:pos + 3]
                if codon in table.stop_codons:
                    if begin is not None and pos + 3 - begin >= min_nt:
                        start, end = (begin, pos + 3) if strand == 1 else (n - pos - 3, n - begin)
                        product = str(Seq(oriented[begin:pos]).translate(table=table.id))
                        found.append({"start": start, "end": end, "strand": strand,
                                      "frame": strand * (offset + 1), "length_nt": end - start,
                                      "protein": "M" + product[1:], "stop_codon": codon})
                        if len(found) > 2000:
                            raise ValueError("More than 2,000 ORFs. Increase minimum ORF length.")
                    begin = None
                elif begin is None and codon in starts:
                    begin = pos
    return sorted(found, key=lambda row: (row["start"], row["strand"], row["frame"]))

def analyze(sequence, kind, params):
    counts = dict(sorted(Counter(sequence).items()))
    result = {"length": len(sequence), "kind": kind, "counts": counts,
              "entropy_bits": -sum((v / len(sequence)) * log2(v / len(sequence)) for v in counts.values()),
              "warnings": [], "versions": {"biopython": bio_version, "seq_lab": "0.1.0"}}
    if kind == "Protein":
        return protein(sequence, params, result)
    dna = sequence.replace("U", "T")
    canonical = sum(counts.get(base, 0) for base in ("ACGU" if kind == "RNA" else "ACGT"))
    gc_count = counts.get("G", 0) + counts.get("C", 0)
    result.update({"canonical": canonical, "ambiguous": len(sequence) - canonical,
                   "gc_percent": 100 * gc_count / canonical if canonical else None,
                   "at_percent": 100 * (canonical - gc_count) / canonical if canonical else None,
                   "gc_total_percent": 100 * gc_count / len(sequence),
                   "windows": windows(sequence, params["window"], params["step"]),
                   "dinucleotides": dict(sorted(Counter(sequence[i:i+2] for i in range(len(sequence)-1)).items())),
                   "reverse_complement": str(Seq(sequence).reverse_complement_rna() if kind == "RNA" else Seq(sequence).reverse_complement()),
                   "converted": dna if kind == "RNA" else str(Seq(sequence).transcribe())})
    table_id = params["genetic_code"]
    allowed = {item["id"] for item in genetic_codes()}
    if table_id not in allowed:
        raise ValueError("Unsupported genetic code. Context-dependent stop tables are excluded.")
    table = CodonTable.unambiguous_dna_by_id[table_id]
    starts = [x.upper().replace("U", "T") for x in params["start_codons"]]
    if not starts or any(x not in table.start_codons for x in starts):
        raise ValueError("Start codons must be valid initiation codons for the selected genetic code.")
    translations = []
    for strand, oriented in [(1, dna), (-1, str(Seq(dna).reverse_complement()))]:
        for offset in range(3):
            segment = oriented[offset:]
            complete = len(segment) // 3 * 3
            translations.append({"frame": strand * (offset + 1),
                                 "protein": str(Seq(segment[:complete]).translate(table=table_id)),
                                 "partial_bases": len(segment) - complete})
    result["translations"] = translations
    result["orfs"] = find_orfs(dna, table, params["min_orf_nt"], starts)
    result["method"] = "GC = 100 × (G+C)/(A+C+G+T/U); ambiguous bases excluded. Full windows only. ORFs: first allowed start per stop-delimited frame, including terminal stop in coordinates; linear sequence, six frames."
    if result["ambiguous"]:
        result["warnings"].append("Ambiguous bases are preserved and excluded from GC denominators. Ambiguous codons may translate to X; ORF boundaries require exact start/stop codons.")
    if not result["windows"]:
        result["warnings"].append("Window exceeds sequence length; reduce window size to produce a profile.")
    result["warnings"].append("ORFs are sequence-based predictions, not validated genes. Incomplete ORFs and circular-origin ORFs are not reported.")
    return result

def protein(sequence, params, result):
    nonstandard = sorted(set(sequence) - set("ACDEFGHIKLMNPQRSTVWY"))
    result["method"] = "Biopython ProtParam: average molecular mass, theoretical pI and charge, empirical instability index, Kyte–Doolittle hydropathy. Protein properties are estimates."
    if nonstandard:
        result["properties"] = None
        result["hydropathy"] = []
        result["charge_curve"] = []
        result["warnings"].append("Physicochemical properties unavailable: nonstandard residues or stop symbols (" + ", ".join(nonstandard) + "). No residues were removed.")
        return result
    tool = ProteinAnalysis(sequence)
    result["properties"] = {
        "molecular_weight_da": tool.molecular_weight(), "isoelectric_point": tool.isoelectric_point(),
        "charge_at_ph": tool.charge_at_pH(params["ph"]), "ph": params["ph"],
        "aromaticity": tool.aromaticity(), "instability_index": tool.instability_index(),
        "gravy": tool.gravy(),
    }
    size = params["hydropathy_window"]
    prefix = [0.0]
    for aa in sequence:
        prefix.append(prefix[-1] + kd[aa])
    result["hydropathy"] = [{"position": i + (size + 1) / 2, "value": (prefix[i+size] - prefix[i]) / size}
                           for i in range(0, max(0, len(sequence)-size+1))]
    result["charge_curve"] = [{"ph": i / 2, "charge": tool.charge_at_pH(i / 2)} for i in range(29)]
    if len(sequence) < size:
        result["warnings"].append("Hydropathy window exceeds sequence length; profile is empty.")
    return result
