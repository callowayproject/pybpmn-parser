# Project-specific Development Guidelines

This document captures practical, project-specific knowledge for contributors to pybpmn-parser. It focuses on how this repository is configured, how to set it up quickly, how to run and scope tests (including examples that were verified locally), and conventions/tools enforced by the repo.


## Environment and Tooling

- Read [../agent-os/product/tech-stack.md] for details on the tech stack used in this project.

## Setup

Use `uv` (recommended):

- Create/activate a virtual environment (optional if you prefer to manage envs yourself):
  - `uv venv`
  - `source .venv/bin/activate`
- Install package with all dev/test/docs groups:
  - `uv sync` (uses `[tool.uv].default-groups = ["dev", "test", "docs"]`)


## Running Tests

Pytest configuration is centralized in `pyproject.toml` under `[tool.pytest.ini_options]`:

- Default addopts include coverage of the `pybpmn_parser` package, branch coverage, and HTML report output to `htmlcov`.
- Non-project directories (e.g., `node_modules`, build artifacts) are excluded via `norecursedirs`.
- Test discovery patterns include: `test_*.py`, `*_test.py`, `tests.py`.

Common invocations:

- Run the full suite:
  - `pytest`
- Run a specific file:
  - `pytest tests/test_validator.py`
- Run a specific test function (node id):
  - `pytest tests/test_validator.py::TestParseXML::test_parse_valid_xml`
- Increase verbosity / show print output:
  - `pytest -vv -s`
- Fail fast on first error:
  - `pytest -x`

Coverage artifacts:

- Terminal summary is shown by default.
- HTML coverage is written to `htmlcov` (open `htmlcov/index.html` in a browser).


### Adding and Running a New Test (Verified Example)

To add a focused test without interacting with the rest of the suite, place it anywhere under `tests/` following discovery patterns.

Example (verified locally) — a minimal test file `tests/test_demo_guidelines.py`:

```python
def test_demo_always_passes():
    assert (1 + 1) == 2
```

Run only this file to validate the local environment and the pytest configuration:

```bash
pytest -q tests/test_demo_guidelines.py
```

Notes from the verified run:

- With the repository’s coverage settings, running a single trivial test still triggers coverage over the package. You may see low coverage percentages for many modules if the tiny test doesn’t import them. This is expected and not an error. The run should still pass.
- If you only want to run a targeted subset regularly while working on a feature, prefer scoping to files or node ids as shown above.

After validating, remove the temporary test so as not to pollute the suite.


## Code Style and Quality Gates

- Black: enforced with `line-length = 119` (see `[tool.black]`).
- Ruff: extensive rule set enabled under `[tool.ruff.lint]` with `preview = true`. Some rules are ignored to keep signal high (see `ignore = [...]`). Use:
  - `ruff format .` (Black-compatible formatting via Ruff)
  - `ruff check . --fix` (autofix lint issues where safe)
- Coverage: configured under `[tool.coverage.*]`. Branch coverage is enabled and files matching `**/test_*.py` are omitted from coverage calculations. There’s no explicit minimum in coverage config, but CI may check coverage trends; keep or add tests accordingly.

Pre-commit hooks (optional but recommended):

- Install once: `pre-commit install`
- Run on all files: `pre-commit run -a`

These hooks run Ruff/Black and other checks before each commit to keep the codebase consistent.


## Project-Specific Notes

- PyBPMN domain packages: The repository includes a large set of data models under `pybpmn_parser/bpmn/...` and a moddle plugin subsystem under `pybpmn_parser/plugins/*` (e.g., `plugins/moddle.py`, `plugins/moddle_types.py`, `plugins/moddle_models/`). If you are iterating on Moddle or plugins, prefer writing isolated tests and scoping your runs to those tests during fast iterations.
- Pytest addopts include coverage over the entire `pybpmn_parser` package. When running very small or isolated tests, expect broad coverage tables with many files at 0% — this is normal and not indicative of a failure.
- The minimum Python version is strict (3.12+). Ensure your local venv matches.
- The project uses `uv` lock files (`uv.lock`) for repeatable installs. If you add or update dependencies, prefer `uv add <pkg>` and commit the updated lock file.


## Troubleshooting

- Pytest picks up too many files or is slow: scope runs (file or node id) and use `-x` to fail fast.
- Coverage shows “No data was collected”: This can occur when you run tests outside the package context or run a test file that doesn’t import any project modules while coverage is set to measure the package. It is safe to ignore for quick smoke checks; for realistic coverage, add tests that import and exercise `pybpmn_parser` modules.
- Import errors: Confirm your venv is active and the project is installed in editable mode (`uv sync` or `pip install -e .[dev,test,docs]`).


## Release/Build Notes

- The project is built with Hatchling (`[build-system]`). Normal Python packaging flows apply (`python -m build` if you have `build` installed), but for most contributors, editable installs suffice during development.
- Project metadata and versioning are controlled via `pyproject.toml` and `pybpmn_parser/__init__.py` (see `[tool.hatch.version]`).


## Quick Command Reference

- Create venv + install all groups: `uv venv && source .venv/bin/activate && uv sync`
- Run tests (full): `pytest`
- Run tests (file): `pytest tests/test_bpmn/test_start_event.py`
- Run tests (single test): `pytest tests/test_validator.py::TestParseXML::test_parse_valid_xml`
- Format: `ruff format .`
- Lint: `ruff check . --fix`
- Pre-commit (install): `pre-commit install`
- Pre-commit (run all): `pre-commit run -a`
