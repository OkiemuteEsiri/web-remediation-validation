import hashlib
from collections import Counter
from .models import ValidationCase, ValidationResult

WEIGHT = {"critical": 90, "high": 75, "medium": 50, "low": 25}


def validate(case: ValidationCase) -> ValidationResult:
    observed = case.observed_control.strip().lower()
    expected = case.expected_control.strip().lower()
    evidence_match = expected == observed
    governance = bool(case.owner and case.validator and case.ticket)

    if case.status == "fixed" and evidence_match and governance:
        disposition, confidence, residual, ready = "validated_fixed", 95, max(5, WEIGHT[case.severity] - 65), True
        rationale = "Observed control matches the defined closure criterion and accountable validation evidence is present."
        action = "Retain evidence and monitor for regression through the normal control lifecycle."
    elif case.status == "fixed":
        disposition, confidence, residual, ready = "closure_blocked", 90, WEIGHT[case.severity], False
        rationale = "The finding is marked fixed, but observed evidence or governance metadata does not satisfy the closure criterion."
        action = "Keep the finding open, correct the remediation or evidence gap, then perform an independent revalidation."
    elif case.status == "risk_accepted":
        disposition, confidence, residual, ready = "risk_acceptance_review", 85, WEIGHT[case.severity], False
        rationale = "Risk acceptance is a governance disposition, not technical remediation evidence."
        action = "Confirm documented approval, expiry, compensating controls and scheduled review; do not label the weakness technically fixed."
    elif case.status == "not_applicable":
        disposition, confidence, residual, ready = "scope_review", 75, 10, False
        rationale = "Not-applicable status requires defensible scope evidence rather than a technical-fix assertion."
        action = "Retain scope rationale and reviewer evidence; reopen if architecture or exposure changes."
    else:
        disposition, confidence, residual, ready = "still_open", 95, WEIGHT[case.severity], False
        rationale = "The remediation case remains open and is not eligible for technical closure."
        action = "Complete remediation and collect fresh post-change evidence before revalidation."

    rid = hashlib.sha256(f"{case.finding_id}|{case.validated_at.isoformat()}|{disposition}".encode()).hexdigest()[:16]
    return ValidationResult(rid, case.finding_id, disposition, confidence, min(100, residual), rationale, action, ready)


def metrics(results: list[ValidationResult]) -> dict:
    c = Counter(r.disposition for r in results)
    return {"cases": len(results), "closure_ready": sum(r.closure_ready for r in results),
            "closure_blocked": c["closure_blocked"], "still_open": c["still_open"],
            "risk_acceptance_review": c["risk_acceptance_review"],
            "highest_residual_risk": max((r.residual_risk for r in results), default=0)}
