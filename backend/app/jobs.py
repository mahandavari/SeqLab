import logging
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import update
from .database import Session, Run, Sequence, now
from .scientific.analysis import analyze

pool = ThreadPoolExecutor(max_workers=2, thread_name_prefix="seq-lab")
logger = logging.getLogger("seq_lab")

def execute(run_id):
    with Session() as db:
        claimed = db.execute(update(Run).where(Run.id == run_id, Run.status == "queued").values(status="running"))
        db.commit()
        if claimed.rowcount != 1:
            return
        run = db.get(Run, run_id)
        seq = db.get(Sequence, run.sequence_id)
        sequence, kind, params = seq.sequence, seq.kind, run.parameters
        db.commit()
    try:
        result = analyze(sequence, kind, params)
        with Session() as db:
            db.execute(update(Run).where(Run.id == run_id, Run.status == "running").values(
                status="completed", result=result, finished_at=now()))
            db.commit()
    except Exception as exc:
        logger.exception("Analysis failed: %s", run_id)
        with Session() as db:
            db.execute(update(Run).where(Run.id == run_id, Run.status == "running").values(
                status="failed", error=str(exc) if isinstance(exc, ValueError) else "Analysis failed; see local server log.", finished_at=now()))
            db.commit()
