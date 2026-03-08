# ACEest Fitness & Gym — DevOps Assignment 1

This repository is a complete starter submission for the course assignment: a small Flask application plus CI/CD artifacts (GitHub Actions and Jenkins pipeline) and containerization with Docker. It demonstrates a development → build → test lifecycle suitable for a junior DevOps engineer assignment.

Repository layout
-----------------

```
.
├─ app.py                 # Flask application (factory create_app)
├─ requirements.txt       # Python dependencies
├─ Dockerfile
├─ .dockerignore
├─ Jenkinsfile
├─ .github/workflows/main.yml
├─ tests/
│  ├─ conftest.py
│  └─ test_app.py
└─ README.md
```

Quick project summary
---------------------
- Web service: Flask app exposing simple endpoints for health, workouts and members.
- Tests: Pytest unit tests that validate application logic and input validation.
- Container: `Dockerfile` builds a lightweight image with `gunicorn` as the WSGI server.
- CI: GitHub Actions workflow that installs dependencies, runs syntax checks and pytest, builds the Docker image, and runs tests inside the container.
- Jenkins: `Jenkinsfile` describing a declarative BUILD pipeline: checkout → install → test → build image.

API reference (endpoints)
-------------------------

1) GET /
   - Purpose: sanity endpoint
   - Response: 200
   - Example:

   ```json
   {"service": "ACEest Fitness & Gym API", "status": "ok"}
   ```

2) GET /health
   - Purpose: health check for monitoring
   - Response: 200
   - Example:

   ```json
   {"status": "healthy"}
   ```

3) GET /workouts
   - Purpose: list all workouts (in-memory store)
   - Response: 200 JSON array

4) POST /workouts
   - Purpose: create a workout
   - Payload: { "name": string, "duration_minutes": number }
   - Success: 201 with created object
   - Validation errors: 400

   Example request:
   ```bash
   curl -s -X POST http://localhost:5000/workouts \
     -H "Content-Type: application/json" \
     -d '{"name":"Morning Cardio","duration_minutes":30}'
   ```

5) GET /members
   - Purpose: list members

6) POST /members
   - Purpose: create a member
   - Payload: { "name": string, "email": string }
   - Validation: email must contain `@`

Running locally (developer quickstart)
-------------------------------------

1) Create a virtualenv and install dependencies:

```bash
cd /Users/kshitizranjan15/Documents/Introduction_To_Deveops_Assignment1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Run the app in development mode (Werkzeug) or run gunicorn for a production-like run:

```bash
# development
python app.py

# production-like
gunicorn "app:create_app()" -b 0.0.0.0:5000 --workers 2
```

3) Open http://localhost:5000/ and exercise endpoints with curl or Postman.

Running tests
-------------

- Run tests locally:

```bash
pytest -q
```

- The repository includes `tests/conftest.py` which makes the project importable to pytest.

- Run tests inside the container (same steps the CI uses):

```bash
docker build -t aceest:local .
docker run --rm aceest:local pytest -q
```

CI/CD details
-------------

GitHub Actions workflow (`.github/workflows/main.yml`):
- Triggers: push, pull_request
- Jobs:
  - build-and-test: set up Python, install deps, syntax check (compileall), run pytest
  - docker-build-and-test: build Docker image (locally in runner) and run pytest inside the container

This satisfies the assignment requirement: Build & Lint (we run compile checks), Docker image assembly, and Automated Testing.

Jenkins BUILD stage
-------------------

- `Jenkinsfile` implements a declarative pipeline with stages:
  - Checkout
  - Install dependencies
  - Run pytest
  - Build Docker image

Notes for Jenkins admins:
- Use an agent with Docker and Python installed, or use a Docker-in-Docker approach.
- Configure credentials and registry settings if you add an image push stage.
- To get test reports in Jenkins, configure pytest to generate JUnit XML (pytest --junitxml=report.xml) and update the `post` section to publish those reports.

Version control & commit guidance (suggested for the assignment)
-------------------------------------------------------------

- Branching:
  - main / master: stable code and CI passing
  - feature/<short-desc>: new features
  - fix/<short-desc>: bugfixes

- Commit messages (conventional style suggestion):
  - feat(api): add workouts POST endpoint
  - fix(validations): return 400 when email invalid
  - ci(actions): run tests inside Docker image

Improving test reports and coverage
----------------------------------

- Add pytest-cov to `requirements.txt` and run `pytest --cov=.` in the CI workflow to measure coverage.
- Add a coverage badge to `README.md` if you publish coverage via Codecov or Coveralls.

Troubleshooting
---------------

- If tests fail locally:
  - Ensure you're using the virtualenv where dependencies are installed.
  - Run `pytest -q -k <test_name>` to run a subset.

- If Docker build fails:
  - Verify Docker daemon is running.
  - Check `.dockerignore` to avoid copying large folders.

- If Jenkins fails to build:
  - Ensure the agent has Docker and Python/pip (or use a build image with those tools).

Extending the project (next steps)
---------------------------------

- Persist data: replace in-memory lists with SQLite and SQLAlchemy (add migrations).
- Add integration tests that start the container and run end-to-end scenarios.
- Add security/lint checks in CI (flake8, bandit) and fail on policy violations.
- Add automated deployment stages (staging -> production) using GitHub Actions or Jenkins pipelines tied to tags/releases.

Contact / help
--------------

If you want me to:
- Push this repository to GitHub and wire the Actions workflow to run on pushes
- Add pytest coverage and JUnit output for Jenkins
- Rework the project into a Python package layout (recommended for larger projects)

Tell me which of the above you'd like me to implement next and I'll make the changes.
