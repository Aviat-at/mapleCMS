## MapleCMS — Copilot / AI agent instructions

This file contains concise, project-specific guidance to help an AI coding agent be productive in the MapleCMS backend.

- Workspace root to inspect: `backend/`
- App entry: `backend/app/main.py` — FastAPI app, lifespan events call `init_db()`/`close_db()`; routers are included with `settings.API_V1_PREFIX`.
- Config: `backend/app/core/config.py` — uses Pydantic v2 + pydantic-settings; environment variables are case-sensitive and `.env` is supported.

Quick facts (why these matter)
- The API is mounted under `/api/v1` (see `API_V1_PREFIX`) and docs live at `/{API_V1_PREFIX}/docs`.
- Default dev DB is SQLite (`DATABASE_URL` default in config) so most local work can run without PostgreSQL.
- Services are async and expect an `AsyncSession` from `get_db()` (see `backend/app/core/database.py`).

Developer workflows & commands (exact)
- Run dev server: `make dev` (calls `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`).
- Install deps: `make install` (runs `pip install -r requirements.txt`).
- Run tests: `make test` → `pytest -v`. Tests are under `backend/tests/` and follow `test_*.py`.
- Run migrations: `make migrate` → `alembic upgrade head`. Create with `alembic revision --autogenerate -m "msg"`.
- Init sample DB: `make init-db` → `python scripts/init_db.py`.
- Lint/format: `make lint`, `make format` (uses `ruff`, `mypy`, and `black`).
- Docker: `make docker-build`, `make docker-up` (uses `docker-compose.yml` in `backend/`).

Project-specific patterns and conventions
- Router layout: each endpoint group lives in `backend/app/api/*.py` (e.g., `articles.py`, `auth.py`). Routers are added in `main.py` using `app.include_router(..., prefix=settings.API_V1_PREFIX)`.
- Service layer: business logic lives in `backend/app/services/*_service.py`. Controllers (routers) call these services and pass the AsyncSession from `get_db()`.
- Models and schemas: SQLAlchemy models are in `backend/app/models/`; Pydantic schemas are in `backend/app/schemas/` (v2-style models — follow existing schema patterns when adding fields).
- Dependencies & auth: shared route dependencies are in `backend/app/core/deps.py`. Use `get_current_user`, `get_current_active_user`, or `require_role("role")` for permission checks. Note the role hierarchy {viewer, author, editor, admin} in `deps.py`.
- Config: change defaults only if needed; local dev relies on `.env` and defaults in `config.py` — don't assume a Postgres DB in dev unless `.env` overrides `DATABASE_URL`.

Integration & external dependencies
- S3: AWS integration exists (boto3/aioboto3) for media uploads. See `backend/app/api/media.py` and `backend/app/core/config.py` for S3-related settings.
- Redis: optional via `REDIS_URL` in config. Not required for running tests locally.
- Migrations: Alembic config and scripts are in `backend/alembic/` — migrations are authoritative source for DB changes.

Small implementation contract (use when adding endpoints)
1. Add Pydantic request/response schemas in `backend/app/schemas/` matching existing style.
2. Add SQLAlchemy model changes in `backend/app/models/` and create an alembic migration.
3. Implement business logic in `backend/app/services/*_service.py` as async functions that accept an `AsyncSession`.
4. Add route in `backend/app/api/<resource>.py`, use `Depends(get_db)` and `Depends(require_role(...))` as needed.
5. Add tests in `backend/tests/` mirroring existing tests (use pytest + httpx, pytest-asyncio).

Examples to follow
- Pagination and filters: `articles.list_articles` accepts `skip`, `limit`, and optional filters — follow this signature for list endpoints.
- Permission checks: `articles.update_article` enforces that authors can only edit their own articles; reuse `require_role` where appropriate.

Quality gates
- Tests: run `make test` or `pytest -q` locally.
- Linters: `make lint`; formatting: `make format`.
- Type hints: mypy is configured; `ignore_missing_imports = true` is set — follow typing where code already uses it.

Where to look for clarification
- API surface and examples: `backend/README.md` and `api-reference.md` (root) for expected endpoints and responses.
- App entry (lifespan, CORS, global exception handler): `backend/app/main.py`.
- Config & defaults: `backend/app/core/config.py`.

If anything here is unclear or missing, tell me which area you want expanded (routing, DB, tests, Docker) and I will update this file.
