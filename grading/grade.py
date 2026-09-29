"""Public feedback reporter. It never replaces the instructor-only grader."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
    "api_correctness": ("tests/test_api.py", 20),
    "persistence_security": ("tests/test_repository_security.py", 15),
    "async_resilience": ("tests/test_async_resilience.py", 15),
    "performance": ("tests/test_performance.py", 10),
    "delivery": ("tests/test_delivery.py", 5),
}


def passes(path: str) -> bool:
    return subprocess.run([sys.executable, "-m", "pytest", "-q", path], cwd=ROOT).returncode == 0


def main() -> None:
    result = {name: points if passes(path) else 0 for name, (path, points) in GROUPS.items()}
    authored = list((ROOT / "student_tests").glob("test_*.py"))
    result["student_tests"] = 5 if authored and any(p.stat().st_size > 100 for p in authored) else 0
    score = sum(result.values())
    result["public_score_out_of_65"] = score - result["student_tests"]
    result["public_score_out_of_70"] = score
    result["note"] = "Final automated grading includes instructor-only contract, security, and scale cases."
    output = ROOT / "grading" / "grade.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
