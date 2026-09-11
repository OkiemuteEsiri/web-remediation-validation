# Web Remediation Validation

An evidence-based Web Application Security and Vulnerability Management project focused on a part of security programs that is often under-engineered: **proving that remediation actually worked**.

Instead of treating `Fixed`, `Done`, or `Risk Accepted` as interchangeable outcomes, this lab models distinct technical and governance dispositions and requires post-change evidence before a vulnerability can be considered closure-ready.

## Problem statement
Finding vulnerabilities is only half of the lifecycle. Weak closure processes create false assurance when tickets are closed without a meaningful retest, compensating controls are confused with remediation, or contradictory evidence is ignored. This project demonstrates a structured remediation-assurance workflow using safe synthetic cases.

## Architecture

```text
Synthetic finding + baseline evidence
              |
              v
      remediation requirement
              |
              v
       expected control state
              |
              v
        observed retest state
              |
              v
   evidence/governance validation
              |
              v
 disposition + residual risk + report
```

## Supported dispositions
| Disposition | Meaning |
|---|---|
| `validated_fixed` | Post-change evidence satisfies the closure criterion |
| `closure_blocked` | Marked fixed, but evidence/governance does not support closure |
| `still_open` | Remediation remains incomplete |
| `risk_acceptance_review` | Risk treatment requiring governance review, not a technical fix |
| `scope_review` | Not-applicable decision requiring defensible scope evidence |

## Key engineering behavior
A case marked `fixed` is not automatically closed. The validator checks the expected control against observed evidence and requires an accountable owner, independent validator and tracking ticket. Contradictory evidence blocks closure.

The bundled synthetic scenario deliberately includes an authorization finding that is marked fixed even though the retest still shows the unwanted behavior. The engine keeps it open rather than trusting workflow status.

## Repository structure

```text
src/
  models.py
  validator.py
  io.py
  reporting.py
  cli.py
data/synthetic_cases.json
tests/test_validator.py
docs/methodology.md
reports/example-validation.md
.github/workflows/ci.yml
```

## Run locally
Python 3.12+ with no third-party dependencies.

```bash
python -m src.cli data/synthetic_cases.json --output validation-report.md
python -m unittest discover -s tests -v
```

## Validation controls
The implementation uses immutable models, timezone-aware validation timestamps, severity/status validation, duplicate finding rejection, deterministic result IDs, bounded residual-risk scoring, explicit closure criteria, evidence-linked rationale, next actions and portfolio metrics.

## ATT&CK context
Synthetic cases can carry ATT&CK mappings such as **T1190 Exploit Public-Facing Application** and **T1078 Valid Accounts**. These mappings provide defensive context and are not assertions that exploitation or compromise occurred.

## Remediation lifecycle
`identify -> reproduce/validate -> define expected control -> remediate -> collect fresh evidence -> independent retest -> residual-risk decision -> evidence-backed closure`

## Risk acceptance
Risk acceptance is deliberately not counted as technical remediation. A mature program should retain approver, business justification, expiry/review date, compensating controls and residual risk, then revisit the decision when conditions change.

## Skills demonstrated
Web application security, vulnerability management, remediation assurance, security governance, Python security automation, evidence handling, risk communication, ATT&CK mapping, unit testing and CI/CD.

## CI
GitHub Actions runs compilation, ten unit tests and an offline CLI smoke test under read-only repository permissions.

## Limitations and safety
This is an offline portfolio lab. It does not send HTTP requests, exploit applications, bypass authorization, capture credentials or target production systems. Real validation must be explicitly authorized and should use the minimum safe test necessary within agreed scope and change windows.

## Roadmap
- Add structured evidence attachments/metadata.
- Add SLA and aging analysis for remediation validation.
- Add approval/expiry fields for risk acceptance.
- Add before/after control diff reporting.
- Add JSON/CSV executive exports.
- Add optional integrations for ticketing systems while preserving evidence-first closure logic.
