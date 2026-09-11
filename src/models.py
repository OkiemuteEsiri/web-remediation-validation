from dataclasses import dataclass
from datetime import datetime

VALID_SEVERITIES = {"critical", "high", "medium", "low"}
VALID_STATUSES = {"open", "fixed", "risk_accepted", "not_applicable"}


def utc(value: str) -> datetime:
    ts = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if ts.tzinfo is None:
        raise ValueError("timestamps must be timezone-aware")
    return ts


@dataclass(frozen=True)
class ValidationCase:
    finding_id: str
    title: str
    severity: str
    asset: str
    owner: str
    original_evidence: str
    remediation: str
    expected_control: str
    observed_control: str
    status: str
    validated_at: datetime
    validator: str
    ticket: str = ""
    attack: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, row: dict) -> "ValidationCase":
        required = ("finding_id", "title", "severity", "asset", "owner", "original_evidence", "remediation", "expected_control", "observed_control", "status", "validated_at", "validator")
        missing = [k for k in required if not str(row.get(k, "")).strip()]
        if missing:
            raise ValueError("missing required fields: " + ", ".join(missing))
        sev, status = str(row["severity"]).lower(), str(row["status"]).lower()
        if sev not in VALID_SEVERITIES: raise ValueError("invalid severity")
        if status not in VALID_STATUSES: raise ValueError("invalid status")
        return cls(str(row["finding_id"]), str(row["title"]), sev, str(row["asset"]), str(row["owner"]),
                   str(row["original_evidence"]), str(row["remediation"]), str(row["expected_control"]),
                   str(row["observed_control"]), status, utc(str(row["validated_at"])), str(row["validator"]),
                   str(row.get("ticket", "")), tuple(str(x) for x in row.get("attack", [])))


@dataclass(frozen=True)
class ValidationResult:
    result_id: str
    finding_id: str
    disposition: str
    confidence: int
    residual_risk: int
    rationale: str
    next_action: str
    closure_ready: bool
