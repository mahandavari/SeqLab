import hashlib
import re
from Bio.Seq import Seq

ALPHABETS = {
    "DNA": set("ACGTRYSWKMBDHVN"),
    "RNA": set("ACGURYSWKMBDHVN"),
    "Protein": set("ACDEFGHIKLMNPQRSTVWYBXZJUO*"),
}
MAX_SEQUENCE = 100_000

def digest(sequence: str) -> str:
    return hashlib.sha256(sequence.encode("ascii")).hexdigest()

def validate(sequence: str, kind: str, normalize: bool = False) -> str:
    if kind not in ALPHABETS:
        raise ValueError("Choose DNA, RNA, or Protein explicitly.")
    if normalize:
        sequence = re.sub(r"\s+", "", sequence).upper()
    if not sequence:
        raise ValueError("Empty sequence record.")
    if len(sequence) > MAX_SEQUENCE:
        raise ValueError("This release supports at most 100,000 symbols per record.")
    invalid = sorted(set(sequence) - ALPHABETS[kind])
    if invalid:
        shown = ", ".join(repr(x) for x in invalid[:12])
        raise ValueError(f"Invalid {kind} symbols: {shown}. Enable normalization for lowercase or spaces; no symbols are discarded.")
    return sequence

def parse_records(text: str, kind: str, normalize: bool, name: str):
    if not text.strip():
        raise ValueError("No sequence data supplied.")
    records = []
    if text.lstrip().startswith(">"):
        header, lines = None, []
        for line in text.splitlines():
            if not line.strip():
                continue
            if line.startswith(">"):
                if header is not None:
                    records.append((header, "\n".join(lines)))
                header, lines = line[1:].strip(), []
                if not header:
                    raise ValueError("A FASTA header is missing its identifier.")
            elif header is None:
                raise ValueError("Unexpected text before the first FASTA header.")
            else:
                lines.append(line)
        if header is not None:
            records.append((header, "\n".join(lines)))
    else:
        if ">" in text or text.startswith("@") or text.startswith("LOCUS"):
            raise ValueError("This import accepts raw sequence or FASTA only.")
        records = [(name.strip(), text)]
    if len(records) > 100:
        raise ValueError("Import at most 100 records per batch.")
    result, seen = [], set()
    for header, raw in records:
        identifier = header.split()[0] if header.split() else ""
        if not identifier or len(header) > 2000:
            raise ValueError("Invalid or excessively long sequence header.")
        if identifier in seen:
            raise ValueError(f"Duplicate identifier: {identifier}. Rename the record before importing.")
        seen.add(identifier)
        # FASTA line breaks are format separators, not biological symbols.
        sequence = validate(raw.replace("\n", "").replace("\r", ""), kind, normalize)
        result.append({"identifier": identifier, "description": header, "sequence": sequence,
                       "kind": kind, "sha256": digest(sequence)})
    return result

def transform(sequence: str, kind: str, operation: str, start=None, end=None, text=None, normalize=False):
    if operation == "edit":
        if text is None:
            raise ValueError("Provide the edited sequence.")
        return validate(text, kind, normalize), kind
    if operation == "subsequence":
        if start is None or end is None or not 0 <= start < end <= len(sequence):
            raise ValueError("Region must satisfy 0 <= start < end <= sequence length.")
        return sequence[start:end], kind
    if operation == "reverse":
        return sequence[::-1], kind
    if kind == "Protein":
        raise ValueError("Complement and transcription are nucleotide operations.")
    seq = Seq(sequence)
    if operation == "complement":
        return str(seq.complement_rna() if kind == "RNA" else seq.complement()), kind
    if operation == "reverse_complement":
        return str(seq.reverse_complement_rna() if kind == "RNA" else seq.reverse_complement()), kind
    if operation == "transcribe" and kind == "DNA":
        return str(seq.transcribe()), "RNA"
    if operation == "back_transcribe" and kind == "RNA":
        return str(seq.back_transcribe()), "DNA"
    raise ValueError("Operation is not applicable to this sequence type.")
