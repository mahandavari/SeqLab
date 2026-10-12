import os
import time
from pathlib import Path

os.environ["SEQ_LAB_DATA"] = str(Path(__file__).resolve().parents[2] / "artifacts" / "test-db")
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

def test_persistence_import_analysis_export():
    Base.metadata.drop_all(engine)
    with TestClient(app) as c:
        p = c.post("/api/projects", json={"title": "Test project"}).json()
        response = c.post(f"/api/projects/{p['id']}/import", json={"text": ">reference\nATGAAATGA", "kind": "DNA"})
        assert response.status_code == 201
        seq = response.json()[0]
        duplicate = c.post(f"/api/projects/{p['id']}/import", json={"text": ">reference\nATG", "kind": "DNA"})
        assert duplicate.status_code == 422
        r = c.post("/api/runs", json={"sequence_id": seq["id"], "min_orf_nt": 6, "window": 3, "step": 3}).json()
        for _ in range(100):
            r = c.get("/api/runs/"+r["id"]).json()
            if r["status"] in ("completed", "failed"):
                break
            time.sleep(.02)
        assert r["status"] == "completed", r
        assert r["result"]["translations"][0]["protein"] == "MK*"
        assert c.get("/api/runs/"+r["id"]+"/export/csv").text.startswith("symbol,count")
        assert "Input SHA-256: " + seq["sha256"] in c.get("/api/runs/"+r["id"]+"/export/html").text
        assert c.get("/api/runs/"+r["id"]+"/export/html").status_code == 200
        derived = c.post("/api/sequences/"+seq["id"]+"/transform", json={"operation":"reverse_complement"}).json()
        assert derived["sequence"] == "TCATTTCAT"
        assert derived["source_id"] == seq["id"]
        bundle = c.get("/api/projects/"+p["id"]+"/export").json()
        assert bundle["sources"][0]["original_text"] == ">reference\nATGAAATGA"
        assert bundle["runs"][0]["input_hash"] == seq["sha256"]
        assert c.get("/api/sequences/"+seq["id"]+"/fasta").text == ">reference\nATGAAATGA\n"
        assert c.post("/api/projects", json={"title": "No"}, headers={"Origin":"https://evil.example"}).status_code == 403
        assert c.post("/api/projects", json={"title": " "}).status_code == 422
        assert c.get("/api/projects/missing/sequences").status_code == 404
    with TestClient(app) as c:
        assert c.get("/api/projects").json()[0]["id"] == p["id"]
        assert len(c.get("/api/projects/"+p["id"]+"/sequences").json()) == 2
        assert c.get("/api/runs/"+r["id"]).json()["status"] == "completed"

def test_cancel_and_restart_recovery(monkeypatch):
    from app import main
    from app.jobs import execute
    monkeypatch.setattr(main.pool, "submit", lambda *args: None)
    with TestClient(app) as c:
        p = c.post("/api/projects", json={"title": "Lifecycle test"}).json()
        s = c.post("/api/projects/"+p["id"]+"/import", json={"text": "ATGAAATGA", "kind": "DNA"}).json()[0]
        cancelled = c.post("/api/runs", json={"sequence_id": s["id"]}).json()
        assert c.post("/api/runs/"+cancelled["id"]+"/cancel", json={}).json()["status"] == "cancelled"
        execute(cancelled["id"])
        assert c.get("/api/runs/"+cancelled["id"]).json()["result"] is None
        failed = c.post("/api/runs", json={"sequence_id": s["id"], "genetic_code": 999}).json()
        execute(failed["id"])
        assert c.get("/api/runs/"+failed["id"]).json()["status"] == "failed"
        pending = c.post("/api/runs", json={"sequence_id": s["id"]}).json()
    with TestClient(app) as c:
        recovered = c.get("/api/runs/"+pending["id"]).json()
        assert recovered["status"] == "failed"
        assert "restart" in recovered["error"]
