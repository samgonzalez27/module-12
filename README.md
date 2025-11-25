# FastAPI Calculator (Module 9)

This repository contains a small FastAPI-based calculator application and a Docker Compose development stack (FastAPI app, PostgreSQL, and pgAdmin). It also includes the project's tests and supporting files.

What I added in this session
- `compose.yaml` — Docker Compose configuration defining three services: `app` (FastAPI), `db` (Postgres), and `pgadmin` (pgAdmin 4). The file uses an env file for secrets and named volumes for persistence.
- `.env` — local environment variables used by the Compose stack (DB credentials, pgAdmin credentials, etc.). Do NOT commit this file.
- `.env.example` — placeholder/example env file safe to commit.
- `.gitignore` — updated to ignore `.env` and common Python artifacts.
- `sql/` (optional) — you can create `sql/schema.sql` or `sql/seeds.sql` to store schema and seed data (recommended).

High-level overview
- FastAPI app: built from the repository `Dockerfile`, available on host port 8000 (mapped by Compose).
- PostgreSQL: Postgres 15 running in `postgres-db`, data persisted in a named Docker volume (`db_data`).
- pgAdmin: Web UI running in `pgadmin` and mapped to host port 5050 so you can open http://localhost:5050.

Environment files
- `.env` contains the runtime secrets/values used by Compose. Example variables:
	- POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
	- DATABASE_URL
	- PGADMIN_DEFAULT_EMAIL, PGADMIN_DEFAULT_PASSWORD
	- FASTAPI_HOST, FASTAPI_PORT
- Keep `.env` out of version control. Commit `.env.example` instead.

Basic commands
- Build and start the stack (detached):

```bash
docker compose up --build -d
```

- Stop the stack but keep volumes (safe):

```bash
docker compose down
```

- Stop the stack and remove volumes (destructive — deletes DB data):

```bash
docker compose down -v
```

- See running containers and port mappings:

```bash
docker ps
```

pgAdmin (web UI)
- Open: http://localhost:5050
- Default login comes from `.env` (PGADMIN_DEFAULT_EMAIL / PGADMIN_DEFAULT_PASSWORD). The admin account is created only on first initialization of the pgAdmin volume. Changing `.env` later will not overwrite an existing pgAdmin admin user unless you remove the `pgadmin` data volume and reinitialize.
- To add your Postgres server inside pgAdmin (from the pgAdmin UI):
	- Host: `db` (this resolves inside Docker; if connecting from your host, use `localhost`)
	- Port: `5432`
	- Username: `postgres` (or value from `.env`)
	- Password: value from `.env`

Working with the database (psql)
- Run SQL from a file:

```bash
docker exec -i postgres-db psql -U postgres -d calculator < sql/schema.sql
```

- Open an interactive psql shell:

```bash
docker exec -it postgres-db psql -U postgres -d calculator
```

- Export schema (schema-only SQL dump):

```bash
docker exec -t postgres-db pg_dump -U postgres -s calculator > sql/schema.sql
```

- Dump data backup:

```bash
docker exec -t postgres-db pg_dump -U postgres calculator > sql/calculator_dump.sql
```

Persistence and volumes
- The Postgres data is stored in a named Docker volume (declared in `compose.yaml` as `db_data`). Running `docker compose down` will not delete the volume by default. To destroy database data you must remove the volume explicitly or run `docker compose down -v`.

Troubleshooting notes from this session
- If Docker Desktop GUI doesn't open from WSL, start Docker Desktop from the Windows Start menu or system tray; WSL may not be able to launch the GUI directly.
- If you see extra unnamed containers (Docker gives random names such as `eager_jemison`), they are likely extra instances of the same image. Use `docker ps` and `docker inspect <name>` to inspect and `docker rm -f <name>` to remove if not needed.
- Browsing to http://localhost:5432 will not work — Postgres uses a binary protocol, not HTTP. Use pgAdmin or psql.

Git and remotes
- If `origin` already exists and you want to point this repository at a new remote, you can replace it:

```bash
git remote set-url origin git@github.com:youruser/your-new-repo.git
```

Or remove then add:

```bash
git remote remove origin
git remote add origin git@github.com:youruser/your-new-repo.git
```

Suggested next steps (optional)
- Commit `sql/schema.sql` and `sql/seeds.sql` into the repo so your schema and seed data are reproducible.
- Add Alembic migrations if your app uses SQLAlchemy and you expect schema changes.
- Create a small README section describing the DB schema (tables, relationships) for graders.

If you want, I can:
- Export the current schema to `sql/schema.sql` and add `sql/seeds.sql` with the current rows.
- Add a short section describing the tables and foreign key relationships discovered during this session.

----

Development quick start

1. Start stack:

```bash
docker compose up --build -d
```

2. Open app: http://localhost:8000
3. Open pgAdmin: http://localhost:5050 (login with `.env` credentials)
4. Connect to DB from pgAdmin using host `db` (or `localhost` from host)

Run tests locally:

```bash
pytest -q
```

Running the new tests
---------------------

- Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

- Run the full test suite (unit + integration):

```bash
./.venv/bin/pytest -q
```

- Run only unit tests (example):

```bash
./.venv/bin/pytest -q tests/test_unit_*.py
```

- Run a single test file (example for the factory tests):

```bash
./.venv/bin/pytest -q tests/test_calculation_factory.py
```

- Run Postgres integration tests locally (they are skipped unless `DATABASE_URL` is set):

Set `DATABASE_URL` to a running Postgres instance and run the tests that require it. Example using Docker Postgres:

```bash
# run a local Postgres container
docker run --name calc-postgres -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=test_db -p 5432:5432 -d postgres:15

# run only the Postgres integration tests
DATABASE_URL=postgresql://test:test@localhost:5432/test_db \
	./.venv/bin/pytest -q tests/test_integration_postgres_calculation.py
```

Integration tests (detailed)
----------------------------

These instructions show how to run integration tests that need a running Postgres instance and how to run the full test suite locally.

- Start a Postgres instance (using Docker Compose or a single container):

```bash
# Option A: start the full Compose stack (recommended for development)
docker compose up --build -d

# Option B: run a single Postgres container (fast, for CI-like tests)
docker run --name calc-postgres -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=test_db -p 5432:5432 -d postgres:15
```

- Wait for Postgres to become ready. A simple, robust way is to retry the connection in a small loop; for quick manual runs a short `sleep` usually suffices:

```bash
sleep 3
```

- Run the integration tests that require Postgres (set `DATABASE_URL` to point at your DB):

```bash
# run all integration tests
DATABASE_URL=postgresql://test:test@localhost:5432/test_db \
	./.venv/bin/pytest -q tests/integration

# run a single Postgres-focused test file
DATABASE_URL=postgresql://test:test@localhost:5432/test_db \
	./.venv/bin/pytest -q tests/test_integration_postgres_calculation.py
```

- Notes:
	- If you used `docker compose up` the service name for the DB in the compose file resolves inside Docker to `db` (or whatever service name is defined in `compose.yaml`). When running tests from your host set `DATABASE_URL` to `postgresql://<user>:<pass>@localhost:<port>/<db>`.
	- The project CI workflow already demonstrates how to start a Postgres service and run the tests; see `.github/workflows/ci-postgres.yml` for the CI setup.

Manual checks via OpenAPI (Swagger UI)
-------------------------------------

FastAPI exposes an interactive OpenAPI UI which is useful for manual verification and exploratory checks.

1. Start the application (either via Uvicorn or Docker Compose):

```bash
# from the project root, with your virtualenv active
uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000

# or via Compose (builds and starts app + db + pgadmin)
docker compose up --build -d
```

2. Open the Swagger UI in your browser:

	- http://127.0.0.1:8000/docs  (Swagger UI)
	- http://127.0.0.1:8000/redoc  (ReDoc)

3. Register a user (via the UI or curl). Example using `curl`:

```bash
curl -s -X POST http://127.0.0.1:8000/users/register \
	-H 'Content-Type: application/json' \
	-d '{"username":"alice","email":"alice@example.com","password":"pw"}' | jq
```

4. Obtain a token (call the token endpoint):

```bash
curl -s -X POST http://127.0.0.1:8000/users/token \
	-H 'Content-Type: application/json' \
	-d '{"username":"alice","password":"pw"}' | jq

# the response contains an `access_token` value
```

5. Authorize in the Swagger UI:

	- Click the **Authorize** button in the top-right of the Swagger UI.
	- The security dialog shows a Bearer token input. Paste the token as either:
		- `Bearer <access_token>`  (include the `Bearer ` prefix), or
		- just the raw token (if the UI accepts it) — either works with this app.

6. Call protected endpoints in the UI (for example `POST /calculations`) and inspect responses.

7. Manual curl example for a protected endpoint (after obtaining `TOKEN`):

```bash
TOKEN="<paste-access-token-here>"
curl -s -X POST http://127.0.0.1:8000/calculations \
	-H 'Content-Type: application/json' \
	-H "Authorization: Bearer ${TOKEN}" \
	-d '{"a":3,"b":4,"type":"add"}' | jq
```

Environment and secrets
-----------------------

- `SECRET_KEY`: set this in your environment for production or CI. The app falls back to a built-in developer secret for local testing, but you should provide a strong `SECRET_KEY` before deploying or publishing images.
- `DATABASE_URL`: used by the SQLAlchemy engine. For integration tests set this to the Postgres connection string as shown above.

Quick checklist for a reproducible local run
------------------------------------------

1. Create and activate the venv, install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

2. Start a Postgres instance (Compose or single container):

```bash
docker compose up --build -d
# or the single-container example shown earlier
```

3. Export env and run tests:

```bash
export DATABASE_URL=postgresql://test:test@localhost:5432/test_db
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
pytest -q
```

If you want, I can also add a short troubleshooting subsection that checks for common issues (port conflicts, Docker permissions, CI caching of dependencies). Let me know if you want that included.

- CI: The repository contains a GitHub Actions workflow (`.github/workflows/ci-postgres.yml`) that starts a Postgres service and runs the full test suite.

Docker Hub image
-----------------

Replace the placeholder below with your Docker Hub image if you push the built image there:

```
docker.io/<your-dockerhub-username>/<repo-name>:<tag>
```

If you want, I can add a short `Makefile` with common commands (start, stop, test, test-postgres) or a `docker-compose.yml` snippet to run Postgres + app + pgAdmin locally.

Submission / Assignment checklist
-------------------------------

Please include the following in your submission (update this README before submitting):

- **GitHub Repository Link**: the URL of this repository (must contain your own code).
- **Docker Hub Repository**: add the link to the Docker Hub repository where your image is pushed (replace the placeholder below):

```
docker.io/<your-dockerhub-username>/<repo-name>:<tag>
```

- **Screenshots required**:
	- **GitHub Actions Workflow**: a screenshot showing a successful workflow run in the repository's **Actions** tab (show the green check and the run details).
	- **Docker Hub Deployment**: a screenshot showing the pushed image/tag on your Docker Hub repository page (show the repository name and the pushed tag).

Helpful commands and notes to produce the screenshots
--------------------------------------------------

- Build and push locally (option A — push from your machine):

```bash
# log in to Docker Hub (follow the prompt)
docker login

# build the image (run from project root)
docker build -t <your-dockerhub-username>/<repo-name>:<tag> .

# push the image to Docker Hub
docker push <your-dockerhub-username>/<repo-name>:<tag>
```

After pushing, open https://hub.docker.com/r/<your-dockerhub-username>/<repo-name> and take the Docker Hub screenshot.

- Push via GitHub Actions (option B — CI-driven push):

1. Add the following repository secrets in GitHub (Settings → Secrets → Actions):
	 - `DOCKERHUB_USERNAME` — your Docker Hub username
	 - `DOCKERHUB_TOKEN` — a Docker Hub access token or password

2. Trigger the workflow by pushing a commit or re-running the action in the Actions tab. When a run completes successfully, take the GitHub Actions screenshot.

Notes & grading tips
-------------------
- If you push locally, include the Docker Hub link in this README and provide the Docker Hub screenshot.
- If you use GitHub Actions to push, include the GitHub Actions screenshot showing the successful `docker push` step and the Docker Hub screenshot showing the new tag.
- A screenshot of Docker Desktop alone is not sufficient for the Docker Hub Deployment requirement — the grader expects to see the image on Docker Hub.

If you want, I can prepare the exact `docker build` and `docker push` command to run locally, or I can help you configure the GitHub Actions secrets and re-run the workflow. Tell me which option you prefer and I'll continue.

License / notes
- This project is for educational purposes. Keep secrets out of source control and use stronger passwords for anything beyond local development.
