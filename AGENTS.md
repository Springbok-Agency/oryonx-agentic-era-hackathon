# Repository Guidelines

## Project Structure & Module Organization
- `app/` holds all agent code; `agent.py` orchestrates flows, creatives live beside it, and shared helpers sit in `app/utils/`.
- `tests/` mirrors the runtime with `unit/`, `integration/`, and `load_test/`; keep fixtures with their suite.
- `deployment/terraform/` manages GCP infrastructure, while `bigquery/` and `notebooks/` capture analytics inputs that feed prompts.
- Root tooling (`Makefile`, `pyproject.toml`, `uv.lock`) governs dependencies; update generated files only via the provided targets.

## Build, Test, and Development Commands
- `make install`: installs uv (if missing) and syncs runtime plus dev dependencies.
- `make playground`: serves the ADK playground on `http://localhost:8501` with live agent reload.
- `make backend`: exports `.requirements.txt` for deploys and launches `app/agent_engine_app.py` as a smoke check.
- `make test`: runs unit and integration suites via `pytest`; set `PYTEST_ADDOPTS="-k <pattern>"` for focused runs.
- `make lint`: executes `codespell`, `ruff check`, `ruff format --check`, and `mypy`; treat failures as blockers.

## Coding Style & Naming Conventions
- Target Python 3.10+, four-space indentation, and Ruff’s 88-character limit; wrap early instead of suppressing warnings.
- Type hints are required; aim for `mypy`-clean runs without new `# type: ignore` markers.
- Use `snake_case` for modules, fixtures, and data files; reserve `PascalCase` for agent classes like `TrendWatcherAgent`.
- Format with `uv run ruff format .` and stage only the intended diffs.

## Testing Guidelines
- Prefer `pytest`; structure files as `test_<feature>.py` with functions named `test_<behavior>` for discovery.
- Keep fast checks in `tests/unit/` and cross-component flows in `tests/integration/`.
- Run `make test` before submitting; follow `tests/load_test/README.md` for Locust checks.
- Cover happy paths, guardrails, and failure signals; note live API stubs in docstrings or fixtures.

## Commit & Pull Request Guidelines
- Write short, imperative commit subjects (`Add PlanReActPlanner ...`) and keep each commit focused.
- Include validation notes (`make test`, `make lint`) and cross-link issues (`Refs #123`) in the body when relevant.
- PRs must state problem, solution, and risk; add screenshots or notebook links when behaviour or data changes.
- Request review from an owning agent teammate and list rollback or follow-up steps in the description.

## Security & Configuration Tips
- Never commit credentials—use `gcloud auth` and store secrets in Terraform variables or GCP Secret Manager.
- Regenerate `.requirements.txt` only through `make backend` to keep deploys reproducible.
- Log new external API scopes or service accounts in `deployment/README.md` before merging.
