# Example Web Remediation Validation

> Illustrative output based entirely on synthetic cases.

## Executive outcome
Four remediation cases demonstrate distinct lifecycle decisions. WEB-001 is eligible for evidence-backed closure. WEB-002 is deliberately marked fixed while its synthetic retest still violates the expected authorization control, so closure must be blocked. WEB-003 remains open. WEB-004 is risk accepted and must remain distinguishable from a technically fixed finding.

## Key assurance decisions
- **WEB-001:** retain closure evidence and monitor for regression.
- **WEB-002:** reopen/rework; a ticket status cannot override contradictory validation evidence.
- **WEB-003:** complete remediation and collect fresh evidence.
- **WEB-004:** verify approval, expiry and compensating controls; do not report as technically fixed.

## Governance principle
A trustworthy remediation program separates technical closure, risk acceptance and scope decisions. Each requires different evidence and reporting treatment.
