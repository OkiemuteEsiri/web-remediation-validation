import unittest
from datetime import datetime, timezone
from src.models import ValidationCase
from src.validator import validate, metrics
from src.reporting import markdown_report


def case(status="fixed", expected="control", observed="control", ticket="T1", severity="high"):
    return ValidationCase("F1", "Synthetic finding", severity, "app.example.test", "owner", "baseline", "fix", expected, observed, status, datetime(2026,1,1,tzinfo=timezone.utc), "validator", ticket, ("T1190",))


class ValidatorTests(unittest.TestCase):
    def test_validated_fixed(self): self.assertTrue(validate(case()).closure_ready)
    def test_fixed_mismatch_blocked(self): self.assertEqual(validate(case(observed="wrong")).disposition, "closure_blocked")
    def test_missing_ticket_blocks_closure(self): self.assertFalse(validate(case(ticket="")).closure_ready)
    def test_open_stays_open(self): self.assertEqual(validate(case(status="open")).disposition, "still_open")
    def test_risk_acceptance_not_fixed(self): self.assertEqual(validate(case(status="risk_accepted")).disposition, "risk_acceptance_review")
    def test_not_applicable_scope_review(self): self.assertEqual(validate(case(status="not_applicable")).disposition, "scope_review")
    def test_residual_risk_bounded(self): self.assertLessEqual(validate(case()).residual_risk, 100)
    def test_deterministic_result_id(self): self.assertEqual(validate(case()).result_id, validate(case()).result_id)
    def test_metrics(self): self.assertEqual(metrics([validate(case())])["closure_ready"], 1)
    def test_report_closure_language(self): self.assertIn("Closure requires evidence", markdown_report([case()], [validate(case())]))


if __name__ == "__main__": unittest.main()
