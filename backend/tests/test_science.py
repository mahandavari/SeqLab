import pytest
from app.schemas import AnalysisInput
from app.scientific.sequences import parse_records, validate, transform
from app.scientific.analysis import analyze, windows

def params(**kwargs):
    return AnalysisInput(sequence_id="test", **kwargs).model_dump(exclude={"sequence_id"})

def test_reference():
    r = analyze("ATGAAATGA", "DNA", params(window=3, step=3, min_orf_nt=6))
    assert r["length"] == 9
    assert r["gc_percent"] == pytest.approx(22.222222)
    assert r["reverse_complement"] == "TCATTTCAT"
    assert r["translations"][0]["protein"] == "MK*"
    assert r["orfs"] == [{"start": 0, "end": 9, "strand": 1, "frame": 1, "length_nt": 9, "protein": "MK", "stop_codon": "TGA"}]

def test_reverse_orf_coordinates():
    r = analyze("GGTCATTTCATCC", "DNA", params(min_orf_nt=6))
    hit = next(o for o in r["orfs"] if o["strand"] == -1)
    assert (hit["start"], hit["end"], hit["protein"]) == (2, 11, "MK")

def test_ambiguity_denominators_and_undefined_windows():
    r = analyze("GCNN", "DNA", params(window=2, step=2))
    assert r["gc_percent"] == 100
    assert r["gc_total_percent"] == 50
    assert r["ambiguous"] == 2
    assert r["windows"][1]["gc"] is None
    assert windows("ATAT", 2, 2)[0]["skew"] is None

def test_window_coordinates_and_partial_tail():
    w = windows("ACGTA", 3, 2)
    assert [(x["start"], x["end"]) for x in w] == [(0, 3), (2, 5)]
    assert w[0]["gc"] == pytest.approx(200/3)

def test_translation_alternative_code_and_partial():
    r = analyze("ATGTGAA", "DNA", params(genetic_code=2))
    assert r["translations"][0] == {"frame": 1, "protein": "MW", "partial_bases": 1}

def test_rna_reverse_complement():
    r = analyze("AUGAAAUGA", "RNA", params())
    assert r["reverse_complement"] == "UCAUUUCAU"
    assert r["translations"][0]["protein"] == "MK*"
    assert r["converted"] == "ATGAAATGA"

@pytest.mark.parametrize("text", ["", ">a\n", ">a\nATG\n>a\nAAA", ">\nATG", "ATG?", "ATGU", "atg", "AT G"])
def test_invalid_imports(text):
    with pytest.raises(ValueError):
        parse_records(text, "DNA", False, "test")

def test_normalization_is_explicit():
    with pytest.raises(ValueError):
        validate("at g", "DNA")
    assert validate("at g", "DNA", True) == "ATG"

def test_multifasta_preserves_identifiers():
    r = parse_records(">abc description\nATG\nAAA\n>def\nCC", "DNA", False, "unused")
    assert r[0]["identifier"] == "abc"
    assert r[0]["description"] == "abc description"
    assert r[0]["sequence"] == "ATGAAA"
    assert r[1]["sequence"] == "CC"

def test_transforms_and_region():
    assert transform("ATGC", "DNA", "subsequence", 1, 3) == ("TG", "DNA")
    assert transform("ATGC", "DNA", "transcribe") == ("AUGC", "RNA")
    assert transform("AUGC", "RNA", "back_transcribe") == ("ATGC", "DNA")
    assert transform("AUGC", "RNA", "complement") == ("UACG", "RNA")
    with pytest.raises(ValueError):
        transform("ATGC", "DNA", "subsequence", 3, 2)

def test_protein_independent_simple_values():
    r = analyze("ACDEFGHIKLMNPQRSTVWY", "Protein", params(hydropathy_window=1))
    assert r["properties"]["aromaticity"] == pytest.approx(3/20)
    assert r["properties"]["molecular_weight_da"] == pytest.approx(2395.7134, abs=.01)
    assert r["hydropathy"][0]["value"] == pytest.approx(1.8)
    assert len(r["charge_curve"]) == 29

def test_protein_documented_reference():
    seq = "MAEGEITTFTALTEKFNLPPGNYKKPKLLYCSNGGHFLRILPDGTVDGTRDRSDQHIQLQLSAESVGEVYIKSTETGQYLAMDTSGLLYGSQTPSEECLFLERLEENHYNTYTSKKHAEKNWFVGLKKNGSCKRGPRTHYGQKAILFLPLPV"
    r = analyze(seq, "Protein", params())
    assert r["properties"]["molecular_weight_da"] == pytest.approx(17103.16, abs=.01)
    assert r["properties"]["isoelectric_point"] == pytest.approx(7.72, abs=.01)

def test_nonstandard_protein_not_silently_stripped():
    r = analyze("MAX*", "Protein", params())
    assert r["length"] == 4
    assert r["properties"] is None
    assert r["counts"]["*"] == 1

def test_invalid_code_starts_and_limit():
    with pytest.raises(ValueError):
        analyze("ATGAAATGA", "DNA", params(genetic_code=27))
    with pytest.raises(ValueError):
        analyze("ATGAAATGA", "DNA", params(start_codons=["AAA"]))
    with pytest.raises(ValueError):
        windows("A"*100_000, 1, 1)

def test_earliest_start_and_alternative_initiation():
    r = analyze("GTGATGAAATAA", "DNA", params(genetic_code=11, start_codons=["GTG", "ATG"], min_orf_nt=6))
    assert any(o["start"] == 0 and o["protein"] == "MMK" for o in r["orfs"])
    assert not any(o["start"] == 3 and o["strand"] == 1 for o in r["orfs"])
