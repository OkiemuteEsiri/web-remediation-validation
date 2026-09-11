# Web Remediation Assurance Methodology

## Objective
The purpose of remediation validation is to establish whether a security weakness is actually resolved—not whether a ticket was moved to Done. This lab models evidence-based closure using synthetic web/application findings.

## Closure standard
A case marked `fixed` is closure-ready only when the observed post-change control exactly satisfies the defined expected control and governance evidence includes an owner, validator and tracking ticket. A status label alone never proves remediation.

## Workflow
`baseline evidence -> remediation requirement -> expected control -> post-change evidence -> independent validation -> residual risk -> closure/rework`

## Dispositions
- **validated_fixed** — technical evidence and governance metadata satisfy closure criteria.
- **closure_blocked** — marked fixed but evidence or governance is insufficient.
- **still_open** — remediation remains incomplete.
- **risk_acceptance_review** — governance treatment; not equivalent to technical remediation.
- **scope_review** — not-applicable decision requiring defensible scope evidence.

## Residual risk
Residual-risk values are deterministic prioritization aids, not CVSS. A validated fix retains a small non-zero value to reinforce that control assurance is contextual and regression remains possible. Risk acceptance retains the original severity weight because the weakness is not technically removed.

## ATT&CK
Synthetic examples may reference T1190 and T1078 for defensive context. ATT&CK mapping does not establish exploitability or compromise.

## Safe validation
This repository does not perform live exploitation or send requests. In real authorized engagements, validation should use the minimum safe test necessary, preserve evidence, respect scope/change windows and avoid destructive techniques.
