from .models import ValidationCase, ValidationResult
from .validator import metrics


def markdown_report(cases: list[ValidationCase], results: list[ValidationResult]) -> str:
    m = metrics(results); by_id = {c.finding_id: c for c in cases}
    lines = ["# Web Remediation Validation Report", "", "> Synthetic, offline remediation-assurance assessment. Closure requires evidence; status labels alone are insufficient.", "",
             "## Executive metrics", "", f"- Cases: **{m['cases']}**", f"- Closure ready: **{m['closure_ready']}**",
             f"- Closure blocked: **{m['closure_blocked']}**", f"- Still open: **{m['still_open']}**",
             f"- Highest residual risk: **{m['highest_residual_risk']}/100**", "", "## Validation decisions", ""]
    for r in results:
        c = by_id[r.finding_id]
        lines += [f"### {c.finding_id} — {c.title}", "", f"- Asset: `{c.asset}`", f"- Severity: **{c.severity.title()}**",
                  f"- Disposition: **{r.disposition}**", f"- Confidence: **{r.confidence}%**", f"- Residual risk: **{r.residual_risk}/100**",
                  f"- Closure ready: **{'yes' if r.closure_ready else 'no'}**", f"- Ticket: `{c.ticket or 'not supplied'}`",
                  f"- ATT&CK context: {', '.join(c.attack) if c.attack else 'not mapped'}", "",
                  f"**Rationale:** {r.rationale}", "", f"**Next action:** {r.next_action}", ""]
    return "\n".join(lines)
