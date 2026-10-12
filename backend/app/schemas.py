from typing import Literal
from pydantic import BaseModel, Field

SequenceKind = Literal["DNA", "RNA", "Protein"]

class ProjectInput(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=2000)

class ImportInput(BaseModel):
    text: str = Field(min_length=1, max_length=1_000_000)
    kind: SequenceKind
    normalize: bool = False
    name: str = Field(default="sequence", min_length=1, max_length=120)

class AnalysisInput(BaseModel):
    sequence_id: str
    window: int = Field(default=50, ge=1, le=100_000)
    step: int = Field(default=10, ge=1, le=100_000)
    genetic_code: int = 1
    min_orf_nt: int = Field(default=30, ge=6, le=100_000)
    start_codons: list[str] = Field(default_factory=lambda: ["ATG"], min_length=1, max_length=10)
    ph: float = Field(default=7.0, ge=0, le=14)
    hydropathy_window: int = Field(default=9, ge=1, le=101)

class TransformInput(BaseModel):
    operation: Literal["reverse", "complement", "reverse_complement", "transcribe", "back_transcribe", "subsequence", "edit"]
    start: int | None = None
    end: int | None = None
    text: str | None = Field(default=None, max_length=100_000)
    normalize: bool = False
