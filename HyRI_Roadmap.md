# HyRI – Roadmap to Human–Agent Research Collaboration (MVP → Beta)

## Phase 0 – Stabilize (1–2 weeks)
- Reproducible dev env: `requirements.txt`/`pyproject`, `.env.example`, makefile.
- Single entrypoint app (Streamlit or FastAPI) with local demo data.
- Logging + error tracking (structlog, Sentry optional).

## Phase 1 – Collaboration Core (2–3 weeks)
- Projects, Artifacts, Threads schema (SQLite/Postgres) with Alembic migrations.
- Agent Orchestrator (LangGraph) with roles: Researcher, Curator, Validator, Editor.
- Human-in-the-loop gates: review/approve steps with UI.
- Provenance tracking: every artifact has sources, agent version, prompts (hash).

## Phase 2 – Validation & QA (2 weeks)
- Claim–evidence linker (span highlights + citations).
- Coverage metrics: % claims with sources; source diversity; date freshness.
- Plagiarism/duplication check; style/format validator for outputs.
- Sanity toolkit: fact-check search, contradiction finder, restricted content filter.

## Phase 3 – Outreach & Sync (2 weeks)
- Email/Calendar templates for collaborator invites (optional: Gmail/Outlook, GCal).
- Drive/Docs sync for shared artifacts; GitHub/ORCID linking.
- Export packs: PDF/Docx/Markdown bundles for reviews.

## Phase 4 – Beta Hardening (ongoing)
- RBAC, audit log, consent + IRB templates.
- Dataset ingestion pipelines with PII scrubbing and licenses.
- CI pipeline, tests >70% coverage on agents/tools; load test with Locust.
