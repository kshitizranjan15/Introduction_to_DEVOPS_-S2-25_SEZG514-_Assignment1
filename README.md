# ACEest Fitness & Gym — DevOps Assignment 1

**Course:** Introduction to DevOps (Merged — CSIZG514 / SEZG514 / SEUSZG514) · Second Semester 2025 (S2-25)  
**Institution:** Birla Institute of Technology and Science, Pilani (BITS Pilani)  
**Division:** Work Integrated Learning Programme (WILP)

> 🔗 **GitHub Repository:** [kshitizranjan15/Introduction\_to\_DEVOPS\_-S2-25\_SEZG514-\_Assignment1](https://github.com/kshitizranjan15/Introduction_to_DEVOPS_-S2-25_SEZG514-_Assignment1)

---

## Table of Contents

1. [Student Details](#student-details)
2. [Problem Statement](#problem-statement)
3. [Objective](#objective)
4. [Assignment Phases](#assignment-phases)
   - [Phase 1 — Application Development & Modularization](#phase-1--application-development--modularization)
   - [Phase 2 — Version Control System Strategy](#phase-2--version-control-system-vcs-strategy)
   - [Phase 3 — Unit Testing & Validation Framework](#phase-3--unit-testing--validation-framework)
   - [Phase 4 — Containerization with Docker](#phase-4--containerization-with-docker)
   - [Phase 5 — Jenkins BUILD & Quality Gate](#phase-5--jenkins-build--quality-gate)
   - [Phase 6 — Automated CI/CD Pipeline via GitHub Actions](#phase-6--automated-cicd-pipeline-via-github-actions)
5. [Required Deliverables — Status](#required-deliverables--status)
6. [CI/CD Pipeline — Live Evidence (Screenshots)](#cicd-pipeline--live-evidence-screenshots)
   - [Screenshot 1 — First Push: CI Check In Progress](#screenshot-1--first-push-to-github-ci-check-in-progress)
   - [Screenshot 2 — Second Commit Pushed](#screenshot-2--second-commit-pushed-unit-test-failure-detected)
   - [Screenshot 3 — Unit Tests Pass, Docker Job Fails](#screenshot-3--github-actions-unit-tests-pass-docker-job-fails)
   - [Screenshot 4 — Docker Job Passes](#screenshot-4--github-actions-docker-job-passes)
   - [Screenshot 5 — GitHub Green Checkmark](#screenshot-5--github-green-checkmark-on-commit)
   - [Screenshot 6 — Jenkins Configure Pipeline](#screenshot-6--jenkins-configure-pipeline-scm-from-github)
   - [Screenshot 7 — Jenkins Stage View](#screenshot-7--jenkins-stage-view--all-builds-history)
   - [Screenshot 8 — GitHub Final Green Commit](#screenshot-8--github-final-green-commit-all-ci-passing)
   - [Screenshot 9 — GitHub Commit Line Final State](#screenshot-9--github-commit-line-final-state)
   - [Screenshot 10 — Live App: Root View (Part 1 — Hero + Programs)](#screenshot-10--live-app-root-view-part-1--hero--programs)
   - [Screenshot 11 — Live App: Root View (Part 2 — Program Detail)](#screenshot-11--live-app-root-view-part-2--program-detail-expanded)
   - [Screenshot 12 — Live App: Root View (Part 3 — Workouts & Members)](#screenshot-12--live-app-root-view-part-3--workouts--members)
   - [Screenshot 13 — Live App: Root View (Part 4 — Gym Info & Version Timeline)](#screenshot-13--live-app-root-view-part-4--gym-info--version-timeline)
   - [Screenshot 14 — Live App: Calorie Calculator in Action](#screenshot-14--live-app-calorie-calculator-in-action)
   - [Screenshot 15 — Live App: Logging a Workout](#screenshot-15--live-app-logging-a-workout)
   - [Screenshot 16 — Live App: Registering a Member](#screenshot-16--live-app-registering-a-member)
7. [Repository Structure](#repository-structure)
8. [Local Setup — Developer Quickstart](#local-setup--developer-quickstart)
9. [Running Tests](#running-tests)
10. [API Quick Reference](#api-quick-reference)
11. [Evaluation Criteria Mapping](#evaluation-criteria-mapping)
12. [DevOps Concepts Applied — Learning Outcomes](#devops-concepts-applied--learning-outcomes)
13. [Application Architecture — Deep Dive](#application-architecture--deep-dive)
14. [CI/CD Pipeline — Full Flow Diagram](#cicd-pipeline--full-flow-diagram)
15. [Key Files — Annotated](#key-files--annotated)
16. [Technology Stack Summary](#technology-stack-summary)
17. [Project Evolution — Version History](#project-evolution--version-history)
18. [Security Considerations](#security-considerations)
19. [Troubleshooting](#troubleshooting)
20. [Future Improvements](#future-improvements-beyond-assignment-scope)
21. [Appendix — Useful Commands](#appendix--useful-commands)
22. [Acknowledgements](#acknowledgements)

---

## Student Details

| Field            | Details                                                                         |
|------------------|---------------------------------------------------------------------------------|
| **Name**         | Kshitiz Ranjan                                                                  |
| **Roll Number**  | 2024TM93505                                                                     |
| **Subject**      | Introduction to DevOps                                                          |
| **Subject Code** | CSIZG514 / SEZG514 / SEUSZG514                                                 |
| **Semester**     | Second Semester 2025 (S2-25)                                                    |
| **Division**     | Work Integrated Learning Programme (WILP)                                       |
| **Institution**  | Birla Institute of Technology and Science, Pilani (BITS Pilani)                |
| **Assignment**   | Assignment 1 — Implementing Automated CI/CD Pipelines for ACEest Fitness & Gym |

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

| Method | Endpoint    | Purpose                            | Status |
|--------|-------------|------------------------------------|--------|
| GET    | `/`         | Service sanity check / browser UI | 200    |
| GET    | `/health`   | Health check for monitoring        | 200    |
| GET    | `/workouts` | List all workouts                  | 200    |
| POST   | `/workouts` | Create a new workout               | 201    |
| GET    | `/members`  | List all members                   | 200    |
| POST   | `/members`  | Create a new member                | 201    |

**Design decisions:**
- **`create_app()` factory pattern** — the application can be instantiated cleanly in tests without global application state, making tests deterministic and independent.
- **In-memory stores** (`app.config["WORKOUTS"]`, `app.config["MEMBERS"]`) — keeps scope focused on DevOps concerns; easily replaceable with a persistent database in a later iteration.
- **Browser-aware root endpoint** — detects `Accept: text/html` to serve a Bootstrap UI (`templates/index.html`), while returning JSON to API clients and to the pytest test client (which sends no `Accept` header).
- **Input validation** — POST endpoints return `400 Bad Request` with a descriptive error message when required fields are missing or malformed.

---

### Phase 2 — Version Control System (VCS) Strategy

A Git repository was initialised locally and pushed to a publicly accessible GitHub repository using proper branching and commit conventions.

**Repository:**
[https://github.com/kshitizranjan15/Introduction\_to\_DEVOPS\_-S2-25\_SEZG514-\_Assignment1](https://github.com/kshitizranjan15/Introduction_to_DEVOPS_-S2-25_SEZG514-_Assignment1)

**Branching strategy:**

| Branch type       | Naming convention      | Purpose                         |
|-------------------|------------------------|---------------------------------|
| Stable production | `main`                 | Always deployable; CI must pass |
| Feature dev       | `feature/<short-desc>` | New features (merged via PR)    |
| Bug fixes         | `fix/<short-desc>`     | Bug corrections                 |
| Infrastructure    | `ci/<short-desc>`      | CI/CD or Dockerfile changes     |

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

| Test name                     | What it validates                                                        |
|-------------------------------|--------------------------------------------------------------------------|
| `test_index_and_health`       | Root returns 200 with `status: ok`; `/health` returns `status: healthy` |
| `test_create_and_get_workout` | POST /workouts creates a record; GET /workouts lists it                  |
| `test_workout_validation`     | POST /workouts with missing `duration_minutes` returns 400              |
| `test_create_and_get_member`  | POST /members creates a record; GET /members lists it                   |
| `test_member_validation`      | POST /members with invalid email returns 400                            |

**Confirmed test result (local execution):**

```
5 passed in 0.14s
```

---

### Phase 4 — Containerization with Docker

The Flask application, its dependencies, and its runtime environment are fully encapsulated in a portable Docker image.

**Dockerfile strategy:**

| Layer                   | Detail                                                                         |
|-------------------------|--------------------------------------------------------------------------------|
| Base image              | `python:3.11-slim` — minimal footprint, reduced attack surface                 |
| Environment variables   | `PYTHONUNBUFFERED=1`, `PIP_NO_CACHE_DIR=off`                                  |
| Dependency installation | Pinned `requirements.txt` for reproducible builds                              |
| Production runtime      | `gunicorn` (WSGI server, not the Werkzeug dev server)                         |
| Exposed port            | `5000`                                                                         |
| Tests in image          | `tests/` is **not** excluded from `.dockerignore` so `pytest` runs in CI      |

**Build and run:**

```bash
# Build the image
docker build -t aceest:local .

# Run the application (http://localhost:5000)
docker run --rm -p 5000:5000 aceest:local

# Run tests inside the container (mirrors CI)
docker run --rm aceest:local pytest -q
```

---

### Phase 5 — Jenkins BUILD & Quality Gate

A **Declarative Jenkins Pipeline** (`Jenkinsfile`) is provided at the repository root. Jenkins serves as a secondary automated validation layer — on every push it pulls the latest code, installs dependencies in a clean virtual environment, executes the test suite, and builds the Docker image.

**Jenkins runs locally inside Docker using a custom image (`aceest-jenkins:local`):**

```bash
docker run -d \
  --name aceest-jenkins \
  -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
  aceest-jenkins:local
```

**Pipeline stages:**

| Stage                     | Action                                                       |
|---------------------------|--------------------------------------------------------------|
| **Checkout**              | `checkout scm` — pull latest commit from GitHub              |
| **Setup Python**          | `python3 -m venv .venv`, `pip install -r requirements.txt`  |
| **Lint / Syntax Check**   | `python -m compileall .`                                    |
| **Unit Tests**            | `pytest -q --junitxml=test-results/results.xml`             |
| **Build Docker Image**    | `docker build -t aceest:build-N .`                          |
| **Test Inside Container** | `docker run --rm aceest:build-N pytest -q`                  |

---

### Phase 6 — Automated CI/CD Pipeline via GitHub Actions

**Workflow file:** `.github/workflows/main.yml`

The pipeline triggers on **every push and pull request** to any branch, providing instant feedback to the developer.

**Pipeline architecture:**

```
Push / Pull Request
       |
       v
+---------------------+   passes   +--------------------------+
|   build-and-test    | ---------> |  docker-build-and-test   |
+---------------------+            +--------------------------+
```

**Job 1: `build-and-test`**

| Step                 | Action                              |
|----------------------|-------------------------------------|
| Checkout code        | `actions/checkout@v4`               |
| Set up Python 3.11   | `actions/setup-python@v4`          |
| Install dependencies | `pip install -r requirements.txt`   |
| Syntax / lint check  | `python -m compileall .`            |
| Run unit tests       | `pytest -q`                         |

**Job 2: `docker-build-and-test`** *(depends on job 1)*

| Step                       | Action                                                  |
|----------------------------|---------------------------------------------------------|
| Checkout code              | `actions/checkout@v4`                                   |
| Set up Docker Buildx       | `docker/setup-buildx-action@v2`                        |
| Build Docker image         | `docker/build-push-action@v4` with **`load: true`**    |
| Run tests inside container | `docker run --rm aceest:ci pytest -q`                  |

> **Why `load: true`?** Docker Buildx builds into a build cache but does not load the image into the runner's local Docker daemon by default. Without `load: true`, `docker run aceest:ci` fails with _"Unable to find image"_. This flag ensures the image is available for subsequent `docker run` steps in the same job.

---

## Required Deliverables — Status

| Deliverable                                 | Status                        |
|---------------------------------------------|-------------------------------|
| Flask application with all endpoints        | ✅ Complete                   |
| Version-controlled Git repository on GitHub | ✅ Complete                   |
| Pytest unit tests (5 tests, all passing)    | ✅ Complete                   |
| `Dockerfile` and `.dockerignore`            | ✅ Complete                   |
| `Jenkinsfile` (Declarative pipeline)        | ✅ Complete                   |
| GitHub Actions workflow (push + PR trigger) | ✅ Complete                   |
| Browser UI for manual testing               | ✅ Complete (Bootstrap 5.3.2) |
| README / Project Report                     | ✅ Complete                   |

---

## CI/CD Pipeline — Live Evidence (Screenshots)

The following screenshots document the complete end-to-end CI/CD journey — from the first push to GitHub, through GitHub Actions running in the cloud, to the Jenkins pipeline running locally in Docker. Each screenshot captures a distinct, significant milestone in the pipeline lifecycle.

---

### Screenshot 1 — First Push to GitHub: CI Check In Progress

![GitHub CI check in progress — first push](images/01_github_ci_in_progress.png)

**What this shows:**
Immediately after the very first `git push` to `main`, GitHub detects the `.github/workflows/main.yml` file and triggers the **CI / build-and-test** job automatically. The yellow dot next to commit `07c132d` indicates the check is **in progress**. The pop-up tooltip reads *"1 in progress check — CI / build-and-test (push) — In progress — This check has started..."*.

**Key DevOps concept — Continuous Integration trigger:**
This is the GitHub Actions webhook firing in real time. Every push to any branch triggers the workflow without any manual intervention, giving the developer immediate automated feedback directly on the GitHub commit view.

**Pipeline state at this point:**
```
git push  -->  GitHub webhook fires  -->  Actions runner provisioned  -->  Job 1 started
```

---

### Screenshot 2 — Second Commit Pushed: Unit Test Failure Detected

![GitHub second commit — unit test failing issue](images/02_github_second_commit_pending.png)

**What this shows:**
A second commit (`307ebf6`) was pushed with the message *"S2-25_SEZG514:correcting unit test failing issue"*. The yellow dot shows GitHub Actions has been triggered again for this new push. This captures the iterative fix cycle — the developer identified a failing test from the first run and pushed a corrective commit immediately.

**Key DevOps concept — Shift-left testing and iterative fixing:**
A test failure was caught by CI (not discovered in production), fixed locally, and re-pushed within minutes. The automated pipeline acts as a safety net that enforces quality on every single commit — not just at release time.

---

### Screenshot 3 — GitHub Actions: Unit Tests Pass, Docker Job Fails

![GitHub Actions — build-and-test passes, docker-build-and-test fails](images/03_github_actions_unit_pass_docker_fail.png)

**What this shows:**
The GitHub Actions run for commit `307ebf6` shows a split result:
- ✅ **`build-and-test`** — succeeded in **6 seconds**. All 5 pytest tests passed.
- ❌ **`docker-build-and-test`** — failed. The Docker in-container test step errored.

The expanded **Run tests (pytest)** step clearly shows:
```
Run pytest -q
.....    [100%]
5 passed in 0.13s
```

**Key DevOps concept — Two-stage fail-fast pipeline:**
The pipeline runs unit tests before Docker operations. Here, unit tests pass, allowing execution to reach the Docker stage where a separate issue is isolated. The two stages correctly diagnosed two independent problems without conflating them.

**Root cause of Docker failure:** The `.dockerignore` was excluding the `tests/` directory, so `pytest` inside the container could not find test files. Fixed by removing `tests` from `.dockerignore`.

---

### Screenshot 4 — GitHub Actions: Docker Job Passes

![GitHub Actions — docker-build-and-test job all steps passing](images/04_github_actions_docker_all_pass.png)

**What this shows:**
After fixing the `.dockerignore` issue, the `docker-build-and-test` job now passes in **31 seconds**. All steps are green:

| Step                                  | Status | Time |
|---------------------------------------|--------|------|
| Set up job                            | ✅     | 4s   |
| Checkout                              | ✅     | 0s   |
| Set up QEMU                           | ✅     | 5s   |
| Set up Docker Buildx                  | ✅     | 5s   |
| Build Docker image (for local runner) | ✅     | 12s  |
| Run tests inside container            | ✅     | 1s   |
| Post Build Docker image               | ✅     | 0s   |

**Key DevOps concept — Environment parity:**
The Docker build and in-container test confirm the application works identically inside the container as it does locally, eliminating the classic "works on my machine" problem.

**Fix applied:** `load: true` was added to `docker/build-push-action@v4`. Without it, Buildx builds into an isolated cache but does **not** load the image into the runner's Docker daemon, causing `docker run aceest:ci` to fail with *"Unable to find image"*.

---

### Screenshot 5 — GitHub Green Checkmark on Commit

![GitHub — green checkmark on commit confirming CI passing](images/05_github_green_checkmark.png)

**What this shows:**
The GitHub repository home page showing a **green checkmark** next to the latest commit — *"S2-25_SEZG514:correcting docker test failing issue #3"*. This is visual confirmation that **both CI jobs passed** for this commit. The repository now shows **4 commits** total.

**Key DevOps concept — Green build as quality gate:**
The green checkmark is the artefact of CI — proof, visible to every team member, that this exact commit has passed all automated quality checks. In a production environment, this status gates deployments: no green means no deploy.

---

### Screenshot 6 — Jenkins: Configure Pipeline (SCM from GitHub)

![Jenkins pipeline configuration — SCM from GitHub](images/06_jenkins_configure_pipeline.png)

**What this shows:**
The Jenkins job `aceest-fitness-gym` configured with **"Pipeline script from SCM"** — Jenkins pulls the `Jenkinsfile` directly from the GitHub repository. Key settings visible:

- **SCM:** Git
- **Repository URL:** `https://github.com/kshitizranjan15/Introduction_to_DEVOPS_-S2-25_SEZG514-_Assignment1`
- **Credentials:** None (public repository)
- **Branch Specifier:** `*/main`

**Key DevOps concept — Pipeline as Code:**
By storing the `Jenkinsfile` in Git, the pipeline definition is version-controlled alongside the application code. Any change to the build process goes through the same commit and review workflow as application changes — eliminating undocumented, click-configured Jenkins jobs that cannot be reproduced or audited.

**How Jenkins was set up locally:**
Jenkins runs inside Docker using a custom image (`aceest-jenkins:local`) built from `Dockerfile.jenkins`. The container mounts the host Docker socket so Jenkins can execute Docker commands. A custom `docker-entrypoint.sh` automatically runs `chmod 666 /var/run/docker.sock` on every container start to fix the Docker socket permission issue.

---

### Screenshot 7 — Jenkins: Stage View — All Builds History

![Jenkins Stage View — build history with all 6 stages](images/07_jenkins_stage_view.png)

**What this shows:**
The Jenkins **Stage View** for the `aceest-fitness-gym` job showing **8 build runs** (builds #1 through #8). Builds #7 and #8 are both green (successful). The Stage View columns map directly to the stages in the `Jenkinsfile`:

| Stage                     | Avg Time | Purpose                                           |
|---------------------------|----------|---------------------------------------------------|
| Declarative: Checkout SCM | 1s       | Jenkins internal SCM initialisation               |
| Checkout                  | 958ms    | `checkout scm` — pull latest commit from GitHub   |
| Setup Python              | 5s       | Create `.venv`, `pip install -r requirements.txt` |
| Lint / Syntax Check       | 295ms    | `python -m compileall .` — catch syntax errors    |
| Unit Tests                | 344ms    | `pytest -q` — run all 5 tests                     |
| Build Docker Image        | 7s       | `docker build -t aceest:build-N .`                |
| Test Inside Container     | 451ms    | `docker run --rm aceest:build-N pytest -q`        |
| Declarative: Post Actions | 342ms    | Workspace cleanup via `cleanWs()`                 |

Build #7 tooltip shows commit `657313e` ("S2-25_SEZG514:Docker update") — demonstrating full traceability from Jenkins build number back to the exact Git commit hash.

**Earlier failed builds (#1–#6) represent the debugging journey:**

| Build | Failure reason                                | Fix applied                                  |
|-------|-----------------------------------------------|----------------------------------------------|
| #1–#2 | `permission denied` on Docker socket         | `docker-entrypoint.sh` auto-runs `chmod 666` |
| #3    | `fatal: not in a git directory`              | Disabled lightweight checkout via Jenkins API|
| #4–#6 | Groovy `unexpected token: } @ line 214`      | Rewrote `Jenkinsfile` — removed duplicate block |
| #7–#8 | All stages green ✅                           | —                                            |

---

### Screenshot 8 — GitHub Final Green Commit (All CI Passing)

![GitHub — final commit with green checkmark, all CI passing](images/08_github_final_green_commit.png)

**What this shows:**
The GitHub repository after **11 commits** with the latest commit `657313e` — *"S2-25_SEZG514:Docker update"* — showing a **green checkmark**. At this point, both GitHub Actions jobs and the Jenkins pipeline are all passing successfully.

**What the green checkmark confirms at this final state:**
1. ✅ GitHub Actions `build-and-test` — Python install + 5 pytest tests passed
2. ✅ GitHub Actions `docker-build-and-test` — Docker image built + tests passed inside container
3. ✅ Jenkins pipeline (local) — all 6 stages completed successfully

**The full 11-commit journey:**

| #     | Commit message                                        | What it fixed / introduced                    |
|-------|-------------------------------------------------------|-----------------------------------------------|
| 1     | S2-25_SEZG514:commiting assignment code base          | Initial push — Flask app, Dockerfile, Actions |
| 2     | S2-25_SEZG514:correcting unit test failing issue      | Fixed `conftest.py`, pinned `Werkzeug==2.3.7` |
| 3     | S2-25_SEZG514:correcting docker test failing issue #1 | Added `load: true` to Actions workflow        |
| 4     | S2-25_SEZG514:correcting docker test failing issue #2 | Fixed `.dockerignore` (kept `tests/`)         |
| 5     | S2-25_SEZG514:correcting docker test failing issue #3 | Verified Docker + pytest chain passes         |
| 6–10  | Various Jenkins fixes                                 | Socket perms, checkout, Groovy syntax errors  |
| 11    | S2-25_SEZG514:Docker update                           | Final clean pipeline — all green ✅           |

---

### Screenshot 9 — GitHub Commit Line Final State

![GitHub — final commit line showing green tick on main branch](images/09_github_final_green_line.png)

**What this shows:**
A close-up of the GitHub repository commit line showing the latest commit on `main` with a **green checkmark** — confirming the repository is in a fully passing state. This is the definitive evidence of a working, automated CI/CD pipeline integrated with GitHub.

**Summary of what this green tick represents:**
- Every code change was automatically tested — no manual testing required
- The Docker image was built and validated in an isolated container environment
- Jenkins independently verified the same build pipeline from a local Docker container
- The repository is in a deployable state — any team member can pull `main` and trust it works

---

### Screenshot 10 — Live App: Root View (Part 1 — Hero + Programs)

![ACEest live app — hero banner and training programs section](images/10_Root_view_of_app_part1.png)

**What this shows:**
The live Flask web application running in a browser at `http://localhost:5000`. The top of the page displays the **gold ACEest navbar**, the hero banner introducing the system, and the **Training Programs section** with three colour-coded cards — 🔥 Fat Loss (FL), 💪 Muscle Gain (MG), and 🌱 Beginner (BG). Each card shows the calorie factor and top exercises drawn directly from the original Tkinter version files (v1.0 through v3.2.4).

---

### Screenshot 11 — Live App: Root View (Part 2 — Program Detail Expanded)

![ACEest live app — expanded program workout and nutrition plan](images/11_Root_view_of_app_part2.png)

**What this shows:**
A program card has been clicked, expanding the **program detail panel** below the cards. Two side-by-side dark boxes display the full weekly **Workout Plan** and the **Nutrition Plan** for the selected program — content fetched live from the `GET /programs/<code>` endpoint. This mirrors the original desktop app's workout/diet display tab from Aceestver-1.0 onwards, now delivered as a REST API response.

---

### Screenshot 12 — Live App: Root View (Part 3 — Workouts & Members)

![ACEest live app — workout log and members registration sections](images/12_Root_view_of_app_part3.png)

**What this shows:**
The **Workout Log** section (left) and **Members** section (right) in the dark-themed UI. Both sections show live-updating lists fed by `GET /workouts` and `GET /members`, with a badge count in the card header. The forms on the right allow logging a new workout or registering a new member, which `POST` to the respective API endpoints and refresh the list without a page reload.

---

### Screenshot 13 — Live App: Root View (Part 4 — Gym Info & Version Timeline)

![ACEest live app — gym metrics and version history sections](images/13_Root_view_of_app_part4.png)

**What this shows:**
The bottom of the main page, showing the **Gym Capacity & Metrics** section with three metric boxes (Capacity: 150 users · Area: 10,000 sq ft · Break-even: 250 members) sourced from `GET /gym-info`, followed by the **Version History timeline** charting the evolution of the application from `Aceestver-1.0` (basic Tkinter) through all 10 desktop versions to the final Flask web API with Docker and CI/CD.

---

### Screenshot 14 — Live App: Calorie Calculator in Action

![ACEest live app — calorie calculator showing result](images/14_calorie_calc.png)

**What this shows:**
The **Calorie Calculator** in use. A body weight has been entered and a program selected; after clicking **Calculate**, the result card displays the daily calorie target in large gold text, with the full breakdown formula below it (`weight_kg × factor = kcal/day`). The calculation is performed by the `POST /calories` endpoint using the `calorie_factor` values (FL=22, MG=35, BG=26) sourced directly from Aceestver-1.1 through v3.2.4.

---

### Screenshot 15 — Live App: Logging a Workout

![ACEest live app — workout entry form and live log list](images/15_workout_log_adding.png)

**What this shows:**
A workout being logged via the form. The **workout name** and **duration in minutes** have been entered; upon submission the entry appears instantly in the live list on the left via `POST /workouts`, and the badge counter increments. This demonstrates the in-memory store updating in real time without any page refresh — a feature available across all API-backed sections.

---

### Screenshot 16 — Live App: Registering a Member

![ACEest live app — member registration form with program selection](images/16_register_member.png)

**What this shows:**
The **Register Member** form completed with a member's name, email, and selected training program (FL / MG / BG). On submission, `POST /members` creates the entry and the member appears in the list with a colour-coded program badge — matching the program colours from the original Aceestver desktop suite (🔴 FL, 🟢 MG, 🔵 BG). This closes the loop between the web UI, the REST API, and the original business logic.

---

```
.
├── app.py                               # Flask application — factory create_app()
├── requirements.txt                     # Pinned Python dependencies
├── Dockerfile                           # Container image build instructions
├── Dockerfile.jenkins                   # Custom Jenkins image (Docker CLI + Python3)
├── docker-entrypoint.sh                 # Jenkins container entrypoint (fixes Docker socket)
├── .dockerignore                        # Build context exclusions
├── Jenkinsfile                          # Declarative Jenkins BUILD pipeline
├── .github/
│   └── workflows/
│       └── main.yml                     # GitHub Actions CI/CD workflow
├── tests/
│   ├── conftest.py                      # sys.path setup for pytest
│   └── test_app.py                      # Pytest unit tests (5 tests)
├── templates/
│   └── index.html                       # Browser UI (Bootstrap 5.3.2)
├── images/                              # CI/CD pipeline evidence screenshots
│   ├── 01_github_ci_in_progress.png     # Screenshot 1 — First push, CI in progress
│   ├── 02_github_second_commit_pending.png  # Screenshot 2 — Second commit pending
│   ├── 03_github_actions_unit_pass_docker_fail.png  # Screenshot 3 — Unit pass, Docker fail
│   ├── 04_github_actions_docker_all_pass.png  # Screenshot 4 — Docker job passes
│   ├── 05_github_green_checkmark.png    # Screenshot 5 — GitHub green checkmark
│   ├── 06_jenkins_configure_pipeline.png  # Screenshot 6 — Jenkins pipeline config
│   ├── 07_jenkins_stage_view.png        # Screenshot 7 — Jenkins Stage View all builds
│   ├── 08_github_final_green_commit.png # Screenshot 8 — GitHub final green commit
│   ├── 09_github_final_green_line.png   # Screenshot 9 — GitHub commit line final state
│   ├── 10_Root_view_of_app_part1.png    # Screenshot 10 — Live app hero + programs
│   ├── 11_Root_view_of_app_part2.png    # Screenshot 11 — Live app program detail expanded
│   ├── 12_Root_view_of_app_part3.png    # Screenshot 12 — Live app workouts & members
│   ├── 13_Root_view_of_app_part4.png    # Screenshot 13 — Live app gym info & version timeline
│   ├── 14_calorie_calc.png              # Screenshot 14 — Live app calorie calculator result
│   ├── 15_workout_log_adding.png        # Screenshot 15 — Live app workout log entry
│   └── 16_register_member.png          # Screenshot 16 — Live app member registration
└── README.md                            # This report
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
source .venv/bin/activate

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

| Criterion                      | How this submission addresses it                                                         |
|--------------------------------|------------------------------------------------------------------------------------------|
| **Application Integrity**      | All 6 endpoints respond correctly; validation returns 400 on bad input                  |
| **VCS Maturity**               | Conventional commits, branching strategy, meaningful commit history on GitHub            |
| **Testing Coverage**           | 5 Pytest tests — happy paths and validation for every endpoint; all passing              |
| **Docker Efficiency**          | `python:3.11-slim` base, pinned deps, gunicorn runtime, optimised `.dockerignore`       |
| **Jenkins Pipeline**           | Declarative `Jenkinsfile` with 6 stages; runs locally in Docker; screenshots as evidence |
| **GitHub Actions Reliability** | Both CI jobs pass on push/PR; `load: true` ensures Docker-based tests run correctly     |
| **Documentation Clarity**      | This README covers setup, tests, CI/CD, Jenkins, API reference, and troubleshooting     |

---

## DevOps Concepts Applied — Learning Outcomes

### 1. Shift-Left Testing
Tests run at the **earliest possible stage** — before Docker build, before deployment. Any broken logic is caught in Job 1 of GitHub Actions and in the Jenkins `Unit Tests` stage, long before the image reaches a registry or server.

### 2. Immutable Infrastructure
The Docker image is built fresh on every CI run from a pinned `requirements.txt`. There is no manual installation or configuration on the server — the entire environment is described as code and reproduced identically everywhere.

### 3. Pipeline as Code
Both CI/CD pipelines are version-controlled alongside the application:
- `.github/workflows/main.yml` — GitHub Actions workflow
- `Jenkinsfile` — Jenkins Declarative Pipeline

Pipeline changes go through the same review process as application code changes.

### 4. Fail Fast Principle
The two-job GitHub Actions structure (`build-and-test` → `docker-build-and-test`) implements fail-fast ordering: if unit tests fail, the Docker build job never starts. This saves compute time and gives instant feedback.

### 5. Environment Parity (Dev / CI / Production)

| Environment    | Runtime                         | Port |
|----------------|---------------------------------|------|
| Local dev      | `python app.py` (Flask dev)     | 8000 |
| Docker local   | `gunicorn` inside container     | 5000 |
| GitHub Actions | `gunicorn` in `python:3.11-slim`| 5000 |
| Jenkins        | Same Docker image               | 5000 |

### 6. Declarative over Imperative
The `Jenkinsfile` uses **Declarative Pipeline syntax**. Declarative pipelines are easier to read, enforce a consistent structure, and provide built-in post-build actions (`post { always {} failure {} }`).

---

## Application Architecture — Deep Dive

### Request Routing Diagram

```
                        +----------------------------------+
                        |        Flask Application         |
                        |           (app.py)               |
  Browser               |                                  |
  (Accept: text/html) --+--> GET /  --> templates/         |
                        |            index.html (UI)       |
  API Client / pytest   |                                  |
  (no Accept header) ---+--> GET /  --> JSON response      |
                        |                                  |
  Any client -----------+--> GET /health  --> {"status": "healthy"}
                        |--> GET /workouts --> [list]      |
                        |--> POST /workouts --> {workout}  |
                        |--> GET /members  --> [list]      |
                        |--> POST /members --> {member}    |
                        +----------------------------------+
```

### Data Validation Rules

| Endpoint       | Field              | Rule                       | Error if violated |
|----------------|--------------------|----------------------------|-------------------|
| POST /workouts | `name`             | Required, non-empty string | 400 Bad Request   |
| POST /workouts | `duration_minutes` | Required, positive number  | 400 Bad Request   |
| POST /members  | `name`             | Required, non-empty string | 400 Bad Request   |
| POST /members  | `email`            | Required, must contain `@` | 400 Bad Request   |

---

## CI/CD Pipeline — Full Flow Diagram

```
Developer pushes code to GitHub
           |
           v
  +----------------------------------------------------------+
  |                    GitHub Actions                        |
  |                                                          |
  |  Job 1: build-and-test                                   |
  |  +----------------------------------------------------+  |
  |  |  1. actions/checkout@v4                            |  |
  |  |  2. actions/setup-python@v4  (Python 3.11)        |  |
  |  |  3. pip install -r requirements.txt                |  |
  |  |  4. python -m compileall .  (syntax check)        |  |
  |  |  5. pytest -q               (unit tests)          |  |
  |  +---------------------------+------------------------+  |
  |                              | PASS                      |
  |                              v                           |
  |  Job 2: docker-build-and-test                            |
  |  +----------------------------------------------------+  |
  |  |  1. actions/checkout@v4                            |  |
  |  |  2. docker/setup-buildx-action@v2                 |  |
  |  |  3. docker/build-push-action@v4  (load: true)     |  |
  |  |  4. docker run --rm aceest:ci pytest -q           |  |
  |  +----------------------------------------------------+  |
  +----------------------------------------------------------+
           |
           v  (local Jenkins — triggered manually)
  +--------------------------------------+
  |  Jenkins (Docker container :8080)    |
  |  Stage 1: Checkout                   |
  |  Stage 2: Setup Python               |
  |  Stage 3: Lint / Syntax Check        |
  |  Stage 4: Unit Tests                 |
  |  Stage 5: Build Docker Image         |
  |  Stage 6: Test Inside Container      |
  +--------------------------------------+
```

---

## Key Files — Annotated

### `app.py` — Key sections

```python
def create_app(test_config=None):
    app = Flask(__name__)
    app.config["WORKOUTS"] = []
    app.config["MEMBERS"] = []

    @app.route("/")
    def index():
        # Serve HTML to browsers, JSON to API clients / pytest
        accept = request.headers.get("Accept")
        if accept and "text/html" in accept:
            return render_template("index.html")
        return jsonify({"service": "ACEest Fitness & Gym API", "status": "ok"})
```

### `Dockerfile` — Key sections

```dockerfile
FROM python:3.11-slim          # small, official base image
ENV PYTHONUNBUFFERED=1         # logs appear immediately (no buffering)
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .                       # copies tests/ as well (needed for CI)
EXPOSE 5000
CMD ["gunicorn", "app:create_app()", "-b", "0.0.0.0:5000", "--workers", "2"]
```

### `.github/workflows/main.yml` — Critical fix

```yaml
- name: Build Docker image
  uses: docker/build-push-action@v4
  with:
    context: .
    tags: aceest:ci
    load: true      # REQUIRED: loads image into local daemon for docker run
    push: false
```

---

## Technology Stack Summary

| Component       | Technology               | Version               | Purpose                                  |
|-----------------|--------------------------|-----------------------|------------------------------------------|
| Web framework   | Flask                    | 2.2.5                 | REST API and HTML rendering              |
| WSGI compat     | Werkzeug                 | 2.3.7                 | Pinned for Flask 2.2.x compatibility     |
| Prod server     | Gunicorn                 | 20.1.0                | Multi-worker WSGI server in Docker       |
| Test framework  | Pytest                   | 7.4.0                 | Unit test runner                         |
| Language        | Python                   | 3.11 (Docker) / 3.13 (local) | Application runtime             |
| Container       | Docker                   | 28.4.0                | Image build and run                      |
| Base image      | python:3.11-slim         | —                     | Minimal Debian-based Python image        |
| Frontend UI     | Bootstrap                | 5.3.2 (CDN)           | Responsive browser interface             |
| CI/CD           | GitHub Actions           | —                     | Automated build, test, Docker validation |
| Build pipeline  | Jenkins (Declarative)    | LTS JDK17             | Secondary BUILD & quality gate           |
| VCS             | Git + GitHub             | —                     | Source control and collaboration         |

---

## Project Evolution — Version History

The application was progressively developed from baseline scripts in the `The code versions for DevOps Assignment/` directory:

| Version file         | What it introduced                      |
|----------------------|-----------------------------------------|
| `Aceestver-1.0.py`   | Initial script — basic Python structure |
| `Aceestver-1.1.py`   | Early iteration with minor updates      |
| `Aceestver-2.1.2.py` | Service logic expansion                 |
| `Aceestver-2.2.1.py` | Validation additions                    |
| `Aceestver-2.2.4.py` | Refinements to endpoints                |
| `Aceestver-3.0.1.py` | Modularisation begin                    |
| `Aceestver-3.1.2.py` | Factory pattern introduction            |
| `Aceestver-3.2.4.py` | Production-readiness improvements       |
| `Aceestver1.1.2.py`  | Merged iteration                        |
| `Aceestver2.0.1.py`  | Final pre-DevOps baseline               |
| **`app.py`**         | **Final DevOps-ready Flask application**|

---

## Security Considerations

| Area                  | Practice applied                                                               |
|-----------------------|--------------------------------------------------------------------------------|
| Dependency pinning    | All packages pinned to exact versions — prevents supply-chain drift            |
| No credentials in code| No passwords, API keys, or tokens committed                                   |
| Minimal base image    | `python:3.11-slim` excludes unnecessary OS packages — smaller attack surface   |
| Input validation      | All POST endpoints validate and reject malformed input before processing        |
| `.dockerignore`       | Local virtualenvs, `.git`, and build artefacts excluded from the image context |

---

## Troubleshooting

| Symptom                                       | Root Cause                                 | Fix                                                                     |
|-----------------------------------------------|--------------------------------------------|-------------------------------------------------------------------------|
| `Address already in use` on port 8000         | Another process using the port             | `pkill -f 'python3 app.py'` then restart                               |
| `ModuleNotFoundError: No module named 'app'`  | `PYTHONPATH` not set for pytest            | `tests/conftest.py` handles this automatically                          |
| `no tests ran in 0.00s` inside Docker         | `tests/` was excluded from build context   | Remove `tests` from `.dockerignore`                                    |
| `Unable to find image 'aceest:ci'` in CI      | Buildx image not loaded into runner daemon | Add `load: true` to `docker/build-push-action`                         |
| `MIMEAccept has no attribute 'get'`           | Werkzeug 3.x incompatible with Flask 2.2.5 | Pin `Werkzeug==2.3.7` in `requirements.txt`                            |
| Docker socket `permission denied` in Jenkins  | Socket owned by root                       | `docker-entrypoint.sh` runs `chmod 666 /var/run/docker.sock` on start  |
| Jenkins `Invalid username or password`        | Corrupted bcrypt hash in user config.xml   | Reset hash to known-good bcrypt hash for `admin123`                    |
| Groovy `unexpected token: }` in Jenkinsfile   | Duplicate `pipeline {}` block in file      | Rewrite `Jenkinsfile` from scratch using heredoc                        |

---

## Future Improvements (Beyond Assignment Scope)

| Improvement               | Description                                                             |
|---------------------------|-------------------------------------------------------------------------|
| Persistent database       | Replace in-memory lists with SQLite or PostgreSQL via SQLAlchemy        |
| Authentication            | Add JWT-based authentication for member and workout management          |
| Docker image scanning     | Integrate Trivy or Snyk into the CI pipeline for vulnerability scanning |
| Test coverage reporting   | Add `pytest-cov` and publish HTML coverage reports in GitHub Actions    |
| Container registry push   | Push tagged images to Docker Hub on `main` merge                        |
| Kubernetes deployment     | Add a `k8s/` directory with Deployment and Service manifests            |
| ngrok webhook integration | Expose local Jenkins via ngrok so GitHub can trigger builds via webhook |

---

## Appendix — Useful Commands

```bash
# Check for port conflicts
lsof -t -i:8000

# Syntax-check all Python files
python -m compileall .

# View running containers
docker ps

# Remove all stopped containers
docker container prune -f

# Trigger Jenkins build manually via API
CRUMB=$(curl -s -u "kshitizranjan15:admin123" \
  "http://localhost:8080/crumbIssuer/api/json" \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['crumb'])")
curl -s -u "kshitizranjan15:admin123" -H "Jenkins-Crumb:$CRUMB" \
  -X POST "http://localhost:8080/job/aceest-fitness-gym/build"

# Check last Jenkins build result
curl -s -u "kshitizranjan15:admin123" \
  "http://localhost:8080/job/aceest-fitness-gym/lastBuild/api/json?tree=number,result,building" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); \
    print('Build #'+str(d['number']), '| Result:', d['result'])"
```

---

## Acknowledgements

This project was developed as part of **Assignment 1** for the course **Introduction to DevOps (CSIZG514 / SEZG514 / SEUSZG514)**, Second Semester 2025 (S2-25), under the **Work Integrated Learning Programme (WILP)** at **Birla Institute of Technology and Science, Pilani (BITS Pilani)**.
