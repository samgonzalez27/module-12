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
