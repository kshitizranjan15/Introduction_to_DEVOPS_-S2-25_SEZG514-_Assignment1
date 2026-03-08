# ACEest Fitness & Gym — DevOps Assignment 1

**Course:** Introduction to DevOps (Merged — CSIZG514 / SEZG514 / SEUSZG514) · Second Semester 2025 (S2-25)  
**Institution:** Birla Institute of Technology and Science, Pilani (BITS Pilani)  
**Division:** Work Integrated Learning Programme (WILP)

---

## Student Details

| Field               | Details                                                          |
|---------------------|------------------------------------------------------------------|
| **Name**            | Kshitiz Ranjan                                                   |
| **Roll Number**     | 2024TM93505                                                      |
| **Subject**         | Introduction to DevOps                                           |
| **Subject Code**    | CSIZG514 / SEZG514 / SEUSZG514                                  |
| **Semester**        | Second Semester 2025 (S2-25)                                     |
| **Division**        | Work Integrated Learning Programme (WILP)                        |
| **Institution**     | Birla Institute of Technology and Science, Pilani (BITS Pilani) |
| **Assignment**      | Assignment 1 — Implementing Automated CI/CD Pipelines for ACEest Fitness & Gym |

---

## Problem Statement

You have been appointed as a **Junior DevOps Engineer** for **ACEest Fitness & Gym**, a rapidly scaling startup. Your mission is to architect and implement a robust, automated deployment workflow that guarantees **code integrity**, **environmental consistency**, and **rapid delivery**.

The solution must transition the application through a rigorous lifecycle — from local development to an automated Jenkins BUILD environment.

---

## Objective

This assignment provides comprehensive, hands-on experience in modern DevOps methodologies. By executing this project, students attain professional proficiency in:

- **Version Control** — Git and GitHub
- **Containerization** — Docker
- **CI/CD Orchestration** — GitHub Actions and Jenkins

---

## Assignment Phases

### Phase 1 — Application Development & Modularization

Develop a foundational Flask web application tailored for fitness and gym management, built on baseline Python scripts that initialise core logic and service endpoints.

**Implemented endpoints:**

| Method | Endpoint      | Purpose                               | Status |
|--------|---------------|---------------------------------------|--------|
| GET    | `/`           | Service sanity check / browser UI    | 200    |
| GET    | `/health`     | Health check for monitoring           | 200    |
| GET    | `/workouts`   | List all workouts                     | 200    |
| POST   | `/workouts`   | Create a new workout                  | 201    |
| GET    | `/members`    | List all members                      | 200    |
| POST   | `/members`    | Create a new member                   | 201    |

**Design decisions:**
- **`create_app()` factory pattern** — the application can be instantiated cleanly in tests without global application state, making tests deterministic and independent.
- **In-memory stores** (`app.config["WORKOUTS"]`, `app.config["MEMBERS"]`) — keeps scope focused on DevOps concerns; easily replaceable with a persistent database in a later iteration.
- **Browser-aware root endpoint** — detects `Accept: text/html` to serve a Bootstrap UI (`templates/index.html`), while returning JSON to API clients and to the pytest test client (which sends no `Accept` header).
- **Input validation** — POST endpoints return `400 Bad Request` with a descriptive error message when required fields are missing or malformed.

---

### Phase 2 — Version Control System (VCS) Strategy

A Git repository was initialised locally and pushed to a publicly accessible GitHub repository using proper branching and commit conventions.

**Repository:**
`https://github.com/kshitizranjan15/Introduction_to_DEVOPS_-S2-25_SEZG514-_Assignment1`

**Branching strategy:**

| Branch type         | Naming convention        | Purpose                              |
|---------------------|--------------------------|--------------------------------------|
| Stable production   | `main`                   | Always deployable; CI must pass      |
| Feature development | `feature/<short-desc>`   | New features (merged via PR)         |
| Bug fixes           | `fix/<short-desc>`       | Bug corrections                      |
| Infrastructure      | `ci/<short-desc>`        | CI/CD or Dockerfile changes          |

**Commit message convention (Conventional Commits):**

```
feat(api): add POST /workouts endpoint
fix(validation): return 400 when email has no @ symbol
ci(actions): load Docker image into runner before docker run
docs(readme): add student details and assignment problem statement
```

---

### Phase 3 — Unit Testing & Validation Framework

Pytest is used to implement a suite of unit tests that validate application logic **before** the build stage. Tests act as an automated quality gate — broken logic cannot pass CI.

**File:** `tests/test_app.py`  
**Setup:** `tests/conftest.py` — prepends the repository root to `sys.path` so pytest can import `app` without manually configuring `PYTHONPATH`.

**Tests implemented:**

| Test name                         | What it validates                                               |
|-----------------------------------|-----------------------------------------------------------------|
| `test_index_and_health`           | Root returns 200 with `status: ok`; `/health` returns `status: healthy` |
| `test_create_and_get_workout`     | POST /workouts creates a record; GET /workouts lists it         |
| `test_workout_validation`         | POST /workouts with missing `duration_minutes` returns 400     |
| `test_create_and_get_member`      | POST /members creates a record; GET /members lists it          |
| `test_member_validation`          | POST /members with invalid email returns 400                   |

**Confirmed test result (local execution):**

```
5 passed in 0.14s
```

---

### Phase 4 — Containerization with Docker

The Flask application, its dependencies, and its runtime environment are fully encapsulated in a portable Docker image.

**Dockerfile strategy:**

| Layer                    | Detail                                                          |
|--------------------------|-----------------------------------------------------------------|
| Base image               | `python:3.11-slim` — minimal footprint, reduced attack surface  |
| Environment variables    | `PYTHONUNBUFFERED=1`, `PIP_NO_CACHE_DIR=off`                  |
| Dependency installation  | Pinned `requirements.txt` for reproducible builds              |
| Production runtime       | `gunicorn` (WSGI server, not the Werkzeug dev server)          |
| Exposed port             | `5000`                                                          |
| Tests in image           | `tests/` is **not** excluded from `.dockerignore` so `pytest` runs in CI inside the container |

**Build and run:**

```bash
# Build the image
docker build -t aceest:local .

# Run the application (http://localhost:5000)
docker run --rm -p 5000:5000 aceest:local

# Run tests inside the container (mirrors CI)
docker run --rm aceest:local pytest -q
```

**`.dockerignore` exclusions:**

```
__pycache__ / *.pyc / *.pyo     — Python bytecode
.pytest_cache / .git             — local tooling artefacts
env / venv / build / dist        — local virtualenvs and build artefacts
The code versions for DevOps Assignment  — legacy baseline scripts
```

---

### Phase 5 — Jenkins BUILD & Quality Gate

A **Declarative Jenkins Pipeline** (`Jenkinsfile`) is provided at the repository root. Jenkins serves as a secondary automated validation layer — on every push it pulls the latest code, installs dependencies in a clean environment, executes the test suite, and builds the Docker image.

**Pipeline stages:**

```
Checkout  →  Install  →  Unit Tests  →  Docker Build
```

| Stage             | Action                                           |
|-------------------|--------------------------------------------------|
| **Checkout**      | `checkout scm` — pull latest commit from GitHub  |
| **Install**       | `pip install -r requirements.txt`                |
| **Unit Tests**    | `pytest -q`                                      |
| **Docker Build**  | `docker build -t aceest:jenkins .`               |

**Connecting Jenkins to the repository — SSH deploy key method:**

```bash
# Step 1: Generate an SSH keypair on the Jenkins host
ssh-keygen -t ed25519 -f ~/.ssh/jenkins_deploy -N "" -C "jenkins@aceest"
cat ~/.ssh/jenkins_deploy.pub   # copy this public key
```

| Step | Where                                     | Action                                                               |
|------|-------------------------------------------|----------------------------------------------------------------------|
| 2    | GitHub → repo Settings → Deploy Keys     | Paste the public key; grant read access                              |
| 3    | Jenkins → Credentials                     | Add SSH Username with private key; username: `git`; paste private key |
| 4    | Jenkins job source                        | SSH URL: `git@github.com:kshitizranjan15/Introduction_to_DEVOPS_-S2-25_SEZG514-_Assignment1.git` |
| 5    | GitHub → repo Settings → Webhooks        | Payload URL: `https://<jenkins-host>/github-webhook/`; events: push, PR |

---

### Phase 6 — Automated CI/CD Pipeline via GitHub Actions

**Workflow file:** `.github/workflows/main.yml`

The pipeline triggers on **every push and pull request** to any branch, providing instant feedback to the developer.

**Pipeline architecture:**

```
Push / Pull Request
       │
       ▼
┌─────────────────────┐   passes   ┌──────────────────────────┐
│   build-and-test    │ ─────────► │  docker-build-and-test   │
└─────────────────────┘            └──────────────────────────┘
```

**Job 1: `build-and-test`**

| Step                   | Action                                    |
|------------------------|-------------------------------------------|
| Checkout code          | `actions/checkout@v4`                     |
| Set up Python 3.11     | `actions/setup-python@v4`                |
| Install dependencies   | `pip install -r requirements.txt`         |
| Syntax / lint check    | `python -m compileall .`                  |
| Run unit tests         | `pytest -q`                               |

**Job 2: `docker-build-and-test`** *(depends on job 1)*

| Step                          | Action                                                  |
|-------------------------------|---------------------------------------------------------|
| Checkout code                 | `actions/checkout@v4`                                   |
| Set up Docker Buildx          | `docker/setup-buildx-action@v2`                        |
| Build Docker image            | `docker/build-push-action@v4` with **`load: true`**    |
| Run tests inside container    | `docker run --rm aceest:ci pytest -q`                  |

> **Why `load: true`?** Docker Buildx builds into a build cache but does not load the image into the runner's local Docker daemon by default. Without `load: true`, `docker run aceest:ci` fails with _"Unable to find image"_. This flag ensures the image is available for subsequent `docker run` steps in the same job.

---

## Required Deliverables — Status

| Deliverable                                    | Status             |
|------------------------------------------------|--------------------|
| Flask application with all endpoints           | ✅ Complete        |
| Version-controlled Git repository on GitHub    | ✅ Complete        |
| Pytest unit tests (5 tests, all passing)       | ✅ Complete        |
| `Dockerfile` and `.dockerignore`               | ✅ Complete        |
| `Jenkinsfile` (Declarative pipeline)           | ✅ Complete        |
| GitHub Actions workflow (push + PR trigger)    | ✅ Complete        |
| Browser UI for manual testing                  | ✅ Complete (Bootstrap 5) |
| README / Project Report                        | ✅ Complete        |

---

## Repository Structure

```
.
├─ app.py                          # Flask application — factory create_app()
├─ requirements.txt                # Pinned Python dependencies
├─ Dockerfile                      # Container image build instructions
├─ .dockerignore                   # Build context exclusions
├─ Jenkinsfile                     # Declarative Jenkins BUILD pipeline
├─ .github/
│  └─ workflows/
│     └─ main.yml                  # GitHub Actions CI/CD workflow
├─ tests/
│  ├─ conftest.py                  # sys.path setup for pytest
│  └─ test_app.py                  # Pytest unit tests (5 tests)
├─ templates/
│  └─ index.html                   # Browser UI (Bootstrap 5.3.2)
└─ README.md                       # This report
```

---

## Local Setup — Developer Quickstart

**Prerequisites:** Python 3.11+, Git, Docker (optional for container tests)

```bash
# 1. Clone the repository
git clone https://github.com/kshitizranjan15/Introduction_to_DEVOPS_-S2-25_SEZG514-_Assignment1.git
cd Introduction_to_DEVOPS_-S2-25_SEZG514-_Assignment1

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate         # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
# Open your browser at http://localhost:8000
```

---

## Running Tests

```bash
# Run all tests
pytest -q

# Run a specific test by name
pytest -q -k test_create_and_get_workout

# Verbose output
pytest -v

# Run tests inside Docker container (mirrors CI exactly)
docker build -t aceest:ci .
docker run --rm aceest:ci pytest -q
```

---

## API Quick Reference

```bash
# Health check
curl http://localhost:8000/health

# List workouts
curl http://localhost:8000/workouts

# Create a workout
curl -s -X POST http://localhost:8000/workouts \
  -H "Content-Type: application/json" \
  -d '{"name":"Morning Cardio","duration_minutes":30}'

# List members
curl http://localhost:8000/members

# Create a member
curl -s -X POST http://localhost:8000/members \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}'
```

---

## Evaluation Criteria Mapping

| Criterion                     | How this submission addresses it                                                         |
|-------------------------------|------------------------------------------------------------------------------------------|
| **Application Integrity**     | All 6 endpoints respond correctly; validation returns 400 on bad input                  |
| **VCS Maturity**              | Conventional commits, branching strategy, meaningful commit history on GitHub            |
| **Testing Coverage**          | 5 Pytest tests — happy paths and validation for every endpoint; all passing              |
| **Docker Efficiency**         | `python:3.11-slim` base, pinned deps, gunicorn runtime, optimised `.dockerignore`       |
| **Jenkins Pipeline**          | Declarative `Jenkinsfile` with 4 stages; SSH deploy-key integration fully documented    |
| **GitHub Actions Reliability**| Both CI jobs pass on push/PR; `load: true` ensures Docker-based tests run correctly     |
| **Documentation Clarity**     | This README covers setup, tests, CI/CD, Jenkins, API reference, and troubleshooting     |

---

## Troubleshooting

| Symptom                                            | Root Cause                                        | Fix                                                                                  |
|----------------------------------------------------|---------------------------------------------------|--------------------------------------------------------------------------------------|
| `Address already in use` on port 8000              | Another process using the port                    | `pkill -f 'python3 app.py'` then restart                                            |
| `ModuleNotFoundError: No module named 'app'`       | `PYTHONPATH` not set for pytest                   | `tests/conftest.py` handles this automatically; always run `pytest -q` from repo root |
| `no tests ran in 0.00s` inside Docker              | `tests/` was excluded from build context          | Fixed: `tests` removed from `.dockerignore`                                         |
| `Unable to find image 'aceest:ci'` in CI           | Buildx image not loaded into runner daemon        | Fixed: `load: true` added to `docker/build-push-action`                             |
| `MIMEAccept has no attribute 'get'`                | Werkzeug 3.x incompatible with Flask 2.2.5        | Fixed: `Werkzeug==2.3.7` pinned in `requirements.txt`                               |
| Docker daemon not running locally                  | Docker Desktop not started                        | Start Docker Desktop, then re-run `docker build`                                    |
| Jenkins not triggered by push                      | Webhook URL incorrect or Jenkins not public       | Verify URL ends with `/github-webhook/`; check Recent Deliveries in GitHub Settings → Webhooks |

---

## Appendix — Useful Commands

```bash
# Check for port conflicts
lsof -t -i:8000

# Syntax-check all Python files (mirrors GitHub Actions step)
python -m compileall .

# Generate SSH deploy key for Jenkins
ssh-keygen -t ed25519 -f ~/.ssh/jenkins_deploy -N "" -C "jenkins@aceest"
cat ~/.ssh/jenkins_deploy.pub     # copy this to GitHub repo → Settings → Deploy Keys

# View running containers
docker ps

# Remove all stopped containers
docker container prune -f
```

---

## Acknowledgements

This project was developed as part of **Assignment 1** for the course **Introduction to DevOps (CSIZG514 / SEZG514 / SEUSZG514)**, Second Semester 2025 (S2-25), under the **Work Integrated Learning Programme (WILP)** at **Birla Institute of Technology and Science, Pilani (BITS Pilani)**.
