# HyRI Streamlit App — Next Steps (from demo → serious app)
_Generated 2025-08-24 19:47._

This plan moves the current Streamlit demo toward a robust, multi‑user, observable, and scalable application. It’s organized by phases with clear deliverables and checklists.

---

## Phase 0 — Hardening the Current Demo (1–2 weeks)

**Goals:** Stabilize the app, make runs reproducible, and reduce friction for collaborators.

**Tasks**
- [ ] Add `requirements.txt` (or `pyproject.toml`) with pinned mins for: `streamlit`, `openai`, `anthropic`, `pandas`, `pyttsx3`, `speech_recognition`, `python-dotenv`, `pydantic-settings`, `uvicorn`, `fastapi` (prep for Phase 1).
- [ ] Create `.env.example` and wire `pydantic-settings` for config (env → YAML overrides).
- [ ] Centralize logging (`logging` or `loguru`) with request/session IDs; write logs to file and console.
- [ ] Add error boundaries in Streamlit (user‑friendly messages + bug report link).
- [ ] Minimal **pytest** suite: one smoke test per module + a Streamlit script import test.
- [ ] Add pre‑commit hooks: `black`, `ruff`, `isort`, `end-of-file-fixer`, `trailing-whitespace`.
- [ ] Dockerfile (multi‑stage) + `docker-compose.yml` for local one‑command run.

**Deliverables**
- Reproducible dev setup.
- CI job: lint + tests on push to `main`.

---

## Phase 1 — Split UI and Backend (2–3 weeks)

**Goals:** Keep Streamlit for UI but move all LLM/agent logic into a versioned API service.

**Architecture**
- **Frontend:** Streamlit (kept simple; no heavy business logic).
- **Backend:** FastAPI (`/v1/`) with endpoints:
  - `POST /sessions`: create chat/agent session.
  - `POST /sessions/{{id}}/message`: send input; returns streaming tokens via WebSocket (`/ws`).
  - `GET /sessions/{{id}}`: session state & metadata.
  - `POST /tools/run`: invoke tool skills (e.g., STT/TTS/data ops).

**Tasks**
- [ ] New `backend/` package (FastAPI + uvicorn) and `frontend/` (Streamlit).
- [ ] Add WebSocket streaming from backend → frontend for token‑by‑token output.
- [ ] Define a **Skill Registry**: tools as typed plugins (pydantic models for I/O).
- [ ] Persist session state in Postgres (SQLAlchemy): `users`, `orgs`, `sessions`, `messages`, `runs`.
- [ ] Store heavy artifacts (audio, logs) in object storage (Azure Blob; local `./artifacts/` dev fallback).
- [ ] Introduce **MemoryService** abstraction (Phase 3 will add vector store).

**Deliverables**
- Clear API contracts (OpenAPI.json).
- Streamlit calls FastAPI, not provider SDKs directly.

---

## Phase 2 — Multi‑User Auth & Tenant Isolation (2–3 weeks)

**Goals:** Enable real users and basic org/team separation.

**Tasks**
- [ ] OAuth2/OIDC login (Auth0 or **Azure AD B2C** to align with your Azure track).
- [ ] JWT verification in FastAPI (dependency) and session cookies in Streamlit.
- [ ] RBAC roles: `owner`, `admin`, `member`, `viewer`.
- [ ] Tenant scoping: all queries filtered by `{{org_id, user_id}}`; row‑level policies if using Postgres schemas.
- [ ] Rate limiting + quotas per org/user to control LLM costs.

**Deliverables**
- Multi‑user login, org‑scoped sessions, and **basic subscription tiers** (free/pro).

---

## Phase 3 — Agent Graph Runtime (LangGraph) & Async Jobs (3–4 weeks)

**Goals:** Formalize agents as **graphs** and support long‑running jobs.

**Tasks**
- [ ] Add **LangGraph** (or equivalent) to model agents as nodes with tools/skills.
- [ ] Introduce a **job queue** (Celery/RQ/Arq) backed by Redis for long LLM calls, file processing, STT, etc.
- [ ] Support resumable runs with durable state snapshots (DB rows + blob payloads).
- [ ] Add a **Vector Store** (pgvector on Postgres) for memory & retrieval—wired behind `MemoryService`.
- [ ] Streaming evals/telemetry for each node: latency, token usage, cost breakdown.

**Deliverables**
- Visualizable graph spec per agent (JSON) and reproducible runs with IDs.

---

## Phase 4 — Observability & Ops (2–3 weeks)

**Goals:** See everything; debug quickly; keep costs under control.

**Tasks**
- [ ] Structured logs with trace/span IDs; forward to OpenTelemetry (OTLP).
- [ ] Metrics (Prometheus) + dashboards (Grafana or Azure Monitor) for: request latency, LLM tokens/cost, queue depth, error rates.
- [ ] Central error tracking: Sentry or Azure App Insights.
- [ ] Model governance: prompt/version registry; per‑release changelogs.

**Deliverables**
- Live dashboards; incident‑ready logging; cost reports per org.

---

## Phase 5 — UX Polish & Real‑Time Media (2–4 weeks)

**Goals:** Production‑level interaction patterns and voice/media streaming.

**Tasks**
- [ ] WebSocket‑based token streaming with incremental render (chat bubbles, tool status, partial results).
- [ ] Upload/drag‑drop for files; progress bars; cancel/retry flows.
- [ ] STT/TTS streaming (browser mic → backend; backend TTS → audio player) with fallbacks.
- [ ] Session management UI: search, tags, pinning, export to Markdown/PDF.
- [ ] Access controls on sessions: private/shared/org.

**Deliverables**
- Smooth operator UX; usable for real client demos.

---

## Phase 6 — Security, Privacy, Compliance (ongoing)

**Tasks**
- [ ] Secrets in **Azure Key Vault**; rotate keys; never commit secrets.
- [ ] Data retention policies; PII minimization; per‑tenant encryption at rest where feasible.
- [ ] Audit log for admin actions; IP allowlist options for sensitive orgs.
- [ ] Basic red‑team tests: prompt‑injection, xss/file‑upload sanitization.
- [ ] Model usage policies (safety filters; blocked tools).

---

## Testing & CI/CD (parallel track)

**Tasks**
- [ ] Unit tests (mocks for providers); integration tests (ephemeral Postgres/Redis via `docker-compose` in CI).
- [ ] E2E smoke: Playwright/pytest to click through Streamlit after deploy.
- [ ] GitHub Actions: matrix (3.10–3.12), lint/type/test, build Docker images, deploy to Azure environments.
- [ ] Migrations with Alembic; auto‑apply in CI/preview.

---

## Azure Deployment Blueprint

**Suggested mapping**
- **Frontend (Streamlit):** Azure App Service (Web App for Containers) or Azure Container Apps.
- **Backend (FastAPI):** Azure Container Apps or AKS for higher scale.
- **DB:** Azure Database for PostgreSQL (Flexible Server) with **pgvector**.
- **Cache/Queue:** Azure Cache for Redis.
- **Storage:** Azure Blob for artifacts/logs.
- **Secrets:** Azure Key Vault.
- **Ingress:** Azure Application Gateway; custom domain + HTTPS.
- **Observability:** Azure Monitor (or self‑hosted Prometheus/Grafana).

---

## Repo Restructure (proposed)

```
hyri/
  frontend/                # Streamlit
    app.py
    components/            # custom components
  backend/                 # FastAPI
    main.py
    api/
      v1/
        sessions.py
        tools.py
    services/
      llm_service.py
      memory_service.py
      speech_service.py
      auth_service.py
    models/                # SQLAlchemy
      base.py
      user.py
      org.py
      session.py
      message.py
    workers/               # Celery/RQ tasks
      tasks.py
  common/
    config.py              # pydantic-settings
    logging.py
    schemas.py             # pydantic models
  tests/
    unit/
    integration/
  infra/
    docker/
    k8s/
  docs/
    architecture.md
```

---

## Immediate 10‑Item Hit List (start this week)

1. Add `.env.example`, `requirements.txt`, centralized config (`pydantic-settings`).
2. Create `backend/` FastAPI skeleton with `/healthz` and `/v1/sessions` (in‑memory store).
3. Change Streamlit to call FastAPI for chat; remove direct provider calls from Streamlit.
4. Introduce Postgres via docker‑compose and SQLAlchemy models for `users`, `orgs`, `sessions`, `messages`.
5. Add Redis and a minimal Celery worker; wire a background task (sleep + echo) as a template.
6. Implement WebSocket token streaming in FastAPI and render progressively in Streamlit.
7. Add basic OAuth2 login flow (Auth0 or Azure AD B2C) and protect `/v1/*` endpoints.
8. Set up GitHub Actions: lint + tests; publish Docker images to GHCR.
9. Centralize logs with request/session IDs; write to console + file.
10. Draft `docs/architecture.md` with sequence diagrams for **chat → tools → memory → responses**.

---

## Stretch Ideas (after 1.0)
- **Plugin SDK** for third‑party skills/tools.
- **Evaluation harness** for agents (quality, latency, cost).
- **Team workspaces** with shared memory and granular ACLs.
- **Cost guardrails**: budgets, alerts, auto‑downgrades to cheaper models.
- **Fine‑tuning/LoRA adapters** for domain‑specific agents.

---

**Linkages**
- Complements items in `HyRI-ActionList.md` (deps, tests, CI, docs). This document focuses on _productizing_ the Streamlit experience while keeping the UI lightweight and moving complexity into a scalable backend.
