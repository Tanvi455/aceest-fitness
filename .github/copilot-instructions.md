# ACEest Fitness & Gym project guidance

- Keep the Flask API in `app.py` and create apps through `create_app()` so tests can isolate state.
- Add or update pytest coverage in `tests/` for behavior changes.
- Keep runtime dependencies in `requirements.txt`; put lint and test tools in `requirements-dev.txt`.
- The GitHub Actions workflow and Jenkinsfile should continue to compile, lint, build Docker, and run the containerized tests.
- Validate changes with `python -m compileall -q app.py tests`, `ruff check app.py tests`, and `pytest -q`.
