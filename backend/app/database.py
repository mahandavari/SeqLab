import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from sqlalchemy import create_engine, String, Text, ForeignKey, JSON, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(os.environ.get("SEQ_LAB_DATA", str(ROOT / "data")))
DATA.mkdir(parents=True, exist_ok=True)
engine = create_engine("sqlite:///" + str(DATA / "seq-lab.sqlite3"), connect_args={"check_same_thread": False, "timeout": 30})

@event.listens_for(engine, "connect")
def sqlite_settings(connection, _):
    connection.execute("PRAGMA foreign_keys=ON")
    connection.execute("PRAGMA journal_mode=WAL")

Session = sessionmaker(engine, expire_on_commit=False)
def now():
    return datetime.now(timezone.utc).isoformat()
def uid():
    return str(uuid4())

class Base(DeclarativeBase):
    pass

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[str] = mapped_column(String, default=now)

class Sequence(Base):
    __tablename__ = "sequences"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"))
    identifier: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    sequence: Mapped[str] = mapped_column(Text)
    kind: Mapped[str] = mapped_column(String)
    sha256: Mapped[str] = mapped_column(String)
    source_id: Mapped[str | None] = mapped_column(ForeignKey("sequences.id"), nullable=True)
    provenance: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[str] = mapped_column(String, default=now)

class ImportSource(Base):
    __tablename__ = "import_sources"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"))
    original_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(String, default=now)

class Run(Base):
    __tablename__ = "runs"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"))
    sequence_id: Mapped[str] = mapped_column(ForeignKey("sequences.id"))
    input_hash: Mapped[str] = mapped_column(String)
    parameters: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String, default="queued")
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(String, default=now)
    finished_at: Mapped[str | None] = mapped_column(String, nullable=True)

def serialize(row):
    return {column.name: getattr(row, column.name) for column in row.__table__.columns}
