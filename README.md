# ACEest Fitness & Gym

A small Flask API for checking service health and listing or creating fitness classes.

## Local setup

Requires Python 3.9 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python app.py
```

The API listens on `http://127.0.0.1:5000`.

## API endpoints

- `GET /` returns API information.
- `GET /health` returns the service health status.
- `GET /classes` lists fitness classes.
- `POST /classes` creates a class. Send JSON with `name` and `instructor`; `capacity` is an optional positive integer.
- `GET /classes/<id>` returns one class.

## Run checks

```bash
python -m compileall -q app.py tests
ruff check app.py tests
python -m pytest -q
```

## Docker

Build the production image and run it:

```bash
docker build -t aceest-fitness:latest .
docker run --rm -p 5000:5000 aceest-fitness:latest
```

The Dockerfile's `test` target installs the development dependencies and runs compile, lint, and pytest checks during image assembly:

```bash
docker build --target test -t aceest-fitness:test .
```

## CI/CD

GitHub Actions runs on every push and pull request. It builds the Docker `test` target, which compiles the application, runs Ruff, and executes pytest, then builds the production image.

The Jenkins declarative pipeline in `Jenkinsfile` performs the same Docker test build and then assembles the runtime image. Configure a Jenkins Pipeline job to use this repository and select **Pipeline script from SCM**, Git, the repository URL, and the desired branch. The Jenkins agent needs Docker installed and permission to access the Docker daemon.