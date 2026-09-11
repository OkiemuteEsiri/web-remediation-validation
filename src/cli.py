import argparse
from pathlib import Path
from .io import load_cases
from .reporting import markdown_report
from .validator import validate


def main():
    p = argparse.ArgumentParser(description="Validate web remediation evidence offline")
    p.add_argument("input"); p.add_argument("--output", default="validation-report.md")
    a = p.parse_args(); cases = load_cases(a.input); results = [validate(c) for c in cases]
    Path(a.output).write_text(markdown_report(cases, results), encoding="utf-8")
    print(f"Wrote {a.output} for {len(results)} remediation cases")


if __name__ == "__main__": main()
