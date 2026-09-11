import json
from pathlib import Path
from .models import ValidationCase


def load_cases(path: str) -> list[ValidationCase]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, list): raise ValueError("input must be a JSON array")
    cases = [ValidationCase.from_dict(x) for x in raw]
    ids = [c.finding_id for c in cases]
    if len(ids) != len(set(ids)): raise ValueError("duplicate finding_id")
    return cases
