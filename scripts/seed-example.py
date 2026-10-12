"""Create one clearly labeled instructional example in an otherwise empty workspace."""
import json
import time
from urllib.request import Request, urlopen

BASE = "http://127.0.0.1:8765/api"
def call(path, data=None):
    request = Request(BASE + path, data=json.dumps(data).encode() if data is not None else None,
                      headers={"Content-Type": "application/json"})
    with urlopen(request, timeout=10) as response:
        return json.load(response)

if call("/projects"):
    print("Workspace already has projects; no example was added.")
else:
    project = call("/projects", {"title": "Sequence foundations · example",
                                "description": "Synthetic instructional sequences, not biological reference records."})
    dna = "ATG" + "GCTGACGGTAAATTCGAGCCATAC" * 8 + "TAA" + "CGCGCGATATAT" * 5 + "ATG" + "AAAGGCTTCCAGGAC" * 7 + "TGA"
    sequence = call("/projects/" + project["id"] + "/import",
                    {"kind": "DNA", "text": ">teaching_dna Synthetic instructional DNA; not a natural gene\n" + dna})[0]
    call("/projects/" + project["id"] + "/import",
         {"kind": "Protein", "text": ">teaching_protein Synthetic instructional protein\nMKWVTFISLLFLFSSAYSRGVFRRDTHKSEIAHRFKDLGE"})
    call("/projects/" + project["id"] + "/import",
         {"kind": "RNA", "text": ">teaching_rna Synthetic instructional RNA\nAUGAAAGGCUUCGAGGACUAA"})
    run = call("/runs", {"sequence_id": sequence["id"], "window": 50, "step": 10, "min_orf_nt": 30})
    for _ in range(100):
        status = call("/runs/" + run["id"])
        if status["status"] not in ("queued", "running"):
            break
        time.sleep(.1)
    if status["status"] != "completed":
        raise RuntimeError(status)
    print(json.dumps({"project": project["id"], "run": run["id"], "status": status["status"]}))
