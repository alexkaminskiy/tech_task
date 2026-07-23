# QA Test Task Submission — Alexander Kaminskiy

Two deliverables for the assessment: a manual/exploratory test plan (Task 1) and a coding exercise with unit tests (Task 2).

## Contents

| File | Task | Description |
|---|---|---|
| `reset_password_test_plan_US123456.md` | 1 | Full test plan for the "Reset Password" feature (US #123456) |
| `normalize_code.py` | 2 | `normalize_code` implementation |
| `test_normalize_code.py` | 2 | pytest unit test suite (31 tests) |

## Task 1 — Reset Password Test Plan

docs/`reset_password_test_plan_US123456.md` covers the feature end to end, grouped by category:

1. Positive Testing
2. Negative Testing
3. Boundary & Rate-Limiting Testing (the 5-requests/600s rule)
4. UI / UX Testing
5. Compatibility Testing
6. Monkey / Exploratory Testing

## Task 2 — `normalize_code`

### Running the tests

```bash
# Create virtual environment in root of the cloned project
python -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows CMD)
.venv\Scripts\activate.bat

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Deactivate
deactivate

#install requirements
pip install -r requirements.txt

#Execute tests
pytest -s tests/test_normalize_code.py -v
```

### Summary

`normalize_code(raw: str | None) -> str` normalizes input into a canonical 10-digit code:

1. Trims whitespace.
2. Strips a single leading `N`/`n` prefix (any other leading letter is invalid).
3. Requires the remainder to be non-empty, all ASCII digits, and ≤10 characters.
4. Left-pads to exactly 10 digits.
5. Raises `ValueError` with a specific, human-readable reason for any invalid case (`None`, empty, non-digit, too long, bad prefix).
