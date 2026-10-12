import csv
import html
import io
import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, update
from .database import Base, engine, Session, Project, Sequence, ImportSource, Run, serialize, now
from .schemas import ProjectInput, ImportInput, AnalysisInput, TransformInput
from .scientific.sequences import parse_records, transform, digest
from .scientific.analysis import genetic_codes
from .jobs import pool, execute

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')

@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(engine)
    with Session() as db:
        db.execute(update(Run).where(Run.status.in_(["queued", "running"])).values(
            status="failed", error="Interrupted by application restart. Run the analysis again.", finished_at=now()))
        db.commit()
    yield

app = FastAPI(title="Seq Lab", version="0.1.0", lifespan=lifespan)

@app.middleware("http")
async def local_only(request: Request, call_next):
    host = request.url.hostname
    if host not in {"127.0.0.1", "localhost", "testserver"}:
        return JSONResponse({"detail": "This application is local-only."}, status_code=403)
    origin = request.headers.get("origin")
    if origin and origin not in {"http://127.0.0.1:8765", "http://localhost:8765", "http://127.0.0.1:5173", "http://localhost:5173"}:
        return JSONResponse({"detail": "Cross-origin access is not allowed."}, status_code=403)
    if request.method in {"POST", "PUT", "PATCH"} and not request.headers.get("content-type", "").startswith("application/json"):
        return JSONResponse({"detail": "JSON request required."}, status_code=415)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response

@app.exception_handler(ValueError)
async def invalid_value(request, exc):
    return JSONResponse({"detail": str(exc)}, status_code=422)

def require(db, cls, identity):
    obj = db.get(cls, identity)
    if obj is None:
        raise HTTPException(404, "Record not found.")
    return obj

@app.get("/api/health")
def health():
    return {"application": "seq-lab", "status": "ok", "version": "0.1.0", "storage": "local SQLite", "genetic_codes": genetic_codes()}

@app.get("/api/projects")
def projects():
    with Session() as db:
        return [serialize(p) for p in db.scalars(select(Project).order_by(Project.created_at.desc()))]

@app.post("/api/projects", status_code=201)
def create_project(body: ProjectInput):
    if not body.title.strip():
        raise ValueError("Project title cannot be blank.")
    with Session() as db:
        p = Project(title=body.title.strip(), description=body.description)
        db.add(p)
        db.commit()
        return serialize(p)

@app.patch("/api/projects/{project_id}")
def rename_project(project_id: str, body: ProjectInput):
    if not body.title.strip():
        raise ValueError("Project title cannot be blank.")
    with Session() as db:
        p = require(db, Project, project_id)
        p.title, p.description = body.title.strip(), body.description
        db.commit()
        return serialize(p)

@app.get("/api/projects/{project_id}/sequences")
def sequences(project_id: str):
    with Session() as db:
        require(db, Project, project_id)
        return [serialize(s) for s in db.scalars(select(Sequence).where(Sequence.project_id == project_id).order_by(Sequence.created_at))]

@app.post("/api/projects/{project_id}/import", status_code=201)
def import_sequences(project_id: str, body: ImportInput):
    records = parse_records(body.text, body.kind, body.normalize, body.name)
    with Session() as db:
        require(db, Project, project_id)
        existing = set(db.scalars(select(Sequence.identifier).where(Sequence.project_id == project_id)))
        duplicates = existing & {r["identifier"] for r in records}
        if duplicates:
            raise ValueError("Identifiers already exist in this project: " + ", ".join(sorted(duplicates)))
        source = ImportSource(project_id=project_id, original_text=body.text)
        db.add(source)
        db.flush()
        rows = [Sequence(project_id=project_id, **r, provenance={"import_id": source.id, "normalization": body.normalize}) for r in records]
        db.add_all(rows)
        db.commit()
        return [serialize(s) for s in rows]

@app.post("/api/sequences/{sequence_id}/transform", status_code=201)
def transform_sequence(sequence_id: str, body: TransformInput):
    with Session() as db:
        source = require(db, Sequence, sequence_id)
        text, kind = transform(source.sequence, source.kind, **body.model_dump())
        from .database import uid
        row = Sequence(project_id=source.project_id, identifier=source.identifier + "_" + body.operation + "_" + uid()[:6],
                       description=f"{body.operation} of {source.identifier}", sequence=text, kind=kind,
                       sha256=digest(text), source_id=source.id,
                       provenance={"operation": body.operation, "parameters": body.model_dump(exclude={"text"}), "parent_hash": source.sha256})
        db.add(row)
        db.commit()
        return serialize(row)

@app.post("/api/runs", status_code=202)
def start_run(body: AnalysisInput):
    with Session() as db:
        source = require(db, Sequence, body.sequence_id)
        active = list(db.scalars(select(Run.id).where(Run.status.in_(["queued", "running"]))))
        if len(active) >= 8:
            raise HTTPException(429, "Job queue is full. Wait for a run to finish.")
        run = Run(project_id=source.project_id, sequence_id=source.id, input_hash=source.sha256,
                  parameters=body.model_dump(exclude={"sequence_id"}))
        db.add(run)
        db.commit()
        result = serialize(run)
    pool.submit(execute, result["id"])
    return result

@app.get("/api/projects/{project_id}/runs")
def history(project_id: str):
    with Session() as db:
        require(db, Project, project_id)
        return [{**serialize(r), "result": None} for r in db.scalars(select(Run).where(Run.project_id == project_id).order_by(Run.created_at.desc()))]

@app.get("/api/runs/{run_id}")
def read_run(run_id: str):
    with Session() as db:
        return serialize(require(db, Run, run_id))

@app.post("/api/runs/{run_id}/cancel")
def cancel_run(run_id: str):
    with Session() as db:
        require(db, Run, run_id)
        db.execute(update(Run).where(Run.id == run_id, Run.status.in_(["queued", "running"])).values(status="cancelled", finished_at=now()))
        db.commit()
        return serialize(db.get(Run, run_id))

def download(content, media_type, filename):
    return Response(content, media_type=media_type, headers={"Content-Disposition": f'attachment; filename="{filename}"'})

@app.get("/api/sequences/{sequence_id}/fasta")
def export_fasta(sequence_id: str):
    with Session() as db:
        seq = require(db, Sequence, sequence_id)
        return download(">" + seq.description + "\n" + "\n".join(seq.sequence[i:i+80] for i in range(0, len(seq.sequence), 80)) + "\n",
                        "text/plain", "sequence.fasta")

@app.get("/api/projects/{project_id}/export")
def export_project(project_id: str):
    with Session() as db:
        p = require(db, Project, project_id)
        payload = {"schema_version": 1, "project": serialize(p),
                   "sequences": [serialize(s) for s in db.scalars(select(Sequence).where(Sequence.project_id == project_id))],
                   "sources": [serialize(s) for s in db.scalars(select(ImportSource).where(ImportSource.project_id == project_id))],
                   "runs": [serialize(r) for r in db.scalars(select(Run).where(Run.project_id == project_id))]}
        return download(json.dumps(payload, ensure_ascii=False, indent=2), "application/json", "seq-lab-project.json")

@app.get("/api/runs/{run_id}/export/{format}")
def export_run(run_id: str, format: str):
    with Session() as db:
        run = require(db, Run, run_id)
        seq = require(db, Sequence, run.sequence_id)
        project = require(db, Project, run.project_id)
        payload = serialize(run)
        if format == "json":
            return download(json.dumps(payload, indent=2), "application/json", "analysis.json")
        if not run.result or run.status != "completed":
            raise HTTPException(409, "A completed analysis is required.")
        result = run.result
        if format == "csv":
            output = io.StringIO(newline="")
            writer = csv.writer(output)
            writer.writerow(["symbol", "count", "percent_of_all_symbols"])
            for symbol, count in result["counts"].items():
                writer.writerow([symbol, count, 100 * count / result["length"]])
            return download(output.getvalue(), "text/csv", "composition.csv")
        if format == "windows.csv":
            output = io.StringIO(newline="")
            writer = csv.writer(output)
            writer.writerow(["start_1based", "end_inclusive", "gc_percent", "gc_skew", "canonical_count"])
            for row in result.get("windows", []):
                writer.writerow([row["start"] + 1, row["end"], row["gc"], row["skew"], row["canonical"]])
            return download(output.getvalue(), "text/csv", "gc-windows.csv")
        if format == "html":
            esc = html.escape
            page = '<!doctype html><html lang="en"><meta charset="utf-8"><title>Seq Lab report</title><style>body{font:16px system-ui;max-width:960px;margin:50px auto;color:#172b35}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f1f5f5;padding:20px}h1{color:#087e83}@media print{body{margin:10mm}}</style>'
            page += f'<h1>Seq Lab · {esc(project.title)}</h1><h2>{esc(seq.identifier)}</h2><p>Analysis: {esc(run.created_at)} · {esc(seq.kind)} · {len(seq.sequence)} symbols</p>'
            page += '<h2>Method and limitations</h2><p>' + esc(result["method"]) + '</p><ul>' + ''.join('<li>'+esc(w)+'</li>' for w in result["warnings"]) + '</ul>'
            page += '<h2>Parameters</h2><pre>' + esc(json.dumps(run.parameters, indent=2)) + '</pre><h2>Reproducible results</h2><pre>' + esc(json.dumps(result, indent=2)) + '</pre>'
            page += '<h2>Provenance</h2><p>Input SHA-256: ' + esc(run.input_hash) + '</p><p>Use your browser Print / Save as PDF for a PDF copy.</p></html>'
            return download(page, "text/html", "seq-lab-report.html")
        raise HTTPException(404, "Unsupported export format.")

DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if DIST.exists():
    app.mount("/", StaticFiles(directory=DIST, html=True), name="frontend")
