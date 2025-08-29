# HyRI – ActionList (Deep Dive)

**Scope:** This list compiles urgent fixes, structural refactors, tests, docs, and feature work needed to bring HyRI to a human–agent research collaboration platform.

## 0) Critical / Blocking

- [ ] Add `requirements.txt` (or `pyproject.toml`) with pinned versions; set reproducible envs.

- [ ] Create `README.md` with quickstart, architecture diagram, and troubleshooting.

- [ ] Consolidate Streamlit entrypoints and make a single `streamlit run app.py` path.


## 1) Code Structure & Quality

- [ ] Normalize package layout: `hyri/` with `__init__.py`, `app/`, `agents/`, `services/`, `ui/`.

- [ ] Factor configuration to `config.py` or `pydantic` settings; support `.env` via `python-dotenv`.

- [ ] Replace hard-coded paths/keys with env vars; document `.env.example`.


## 2) Testing & CI

- [ ] Add pytest suite covering: agent orchestration, tool calls, persistence, and error handling.

- [ ] Create test fixtures with synthetic conversations and mock external APIs.

- [ ] Add GitHub Actions: lint (ruff), type-check (mypy/pyright), tests, security scan (bandit).


## 3) Data Layer & Provenance

- [ ] Decide on storage (Postgres/SQLite). Define schema for Projects, Artifacts, Threads, Datasets, Reviews.

- [ ] Add migration tool (alembic). Provide seed script.

- [ ] Implement provenance: every artifact links to source (doc, URL, dataset, agent version, prompt hash).

- [ ] Add content-addressable storage (hash-based) for files and model outputs.


## 4) Agents & Collaboration Workflows

- [ ] Define canonical agent roles: Researcher, Curator, Validator, Editor; codify tools per role.

- [ ] Implement task graph (LangGraph) with checkpoints and retries; persist state.

- [ ] Add human-in-the-loop gates (review/approve/reject) using Streamlit/FastAPI UI components.

- [ ] Add validation tools: citation checker, claim–evidence linker, plagiarism/duplication scanner.

- [ ] Add sanity checks: content policy filter, hallucination meter (source coverage %), unit tests for tools.


## 5) Integrations (Opt-in)

- [ ] Email/Calendar outreach: connect to Gmail/Outlook, Google Calendar; send templated invites to collaborators.

- [ ] Drive/Docs integration: Google Drive/Docs API for shared artifacts; Box/Dropbox optional.

- [ ] ORCID / GitHub linking for researcher identity and repo sync.


## 6) Security, Privacy, Ethics

- [ ] Add role-based access control (RBAC) and project-level permissions.

- [ ] Add audit logging of agent actions and human approvals.

- [ ] Add data retention policy and PII scrubbing pipeline; consent banners and IRB templates.


## 7) UX & Documentation

- [ ] Build onboarding wizard (create project → import sources → choose agents → start run).

- [ ] Add run dashboard: status, errors, validation coverage, pending human actions.

- [ ] Write user guide (how-to collaborate) and developer guide (add a new agent/tool).
