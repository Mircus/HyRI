# HyRI — Hybrid Relational Intelligence Platform

<p align="center">
  <img src="docs/assets/hyri-logo.png" alt="HyRI Logo" width="220"/>
</p>

[![Status](https://img.shields.io/badge/status-active-brightgreen)](#)
[![Python](https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11%20|%203.12-blue)](#)
[![License](https://img.shields.io/badge/license-Apache--2.0-informational)](#license)
[![Tests](https://img.shields.io/badge/tests-pytest-inactive)](#testing)
[![Docs](https://img.shields.io/badge/docs-md-lightgrey)](#documentation)
[![Streamlit](https://img.shields.io/badge/app-streamlit-red)](#run-the-streamlit-app)

HyRI is a **hybrid agent** framework that blends LLMs and tool-augmented skills (speech, TTS, memory, structured reasoning) for **relational intelligence**—agents that can converse, perceive, and act across tasks with traceable state.

---

## 🧭 Overview

- **Agents + Tools:** LLM backends (OpenAI, Anthropic) with skills (speech recognition, TTS, data I/O).
- **Modes:** CLI and Streamlit app for interactive demos.
- **Artifacts:** runs, logs, and configs that make experiments reproducible.

> See also: `docs/neuroglyph_platform_guide.md` for the NeuroGlyph angle.

---

## 🚀 Quickstart

### 1) Clone
```bash
git clone https://github.com/<org>/HyRI.git
cd HyRI
```

### 2) Create and activate env
```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
```

### 3) Install deps
```bash
pip install -r requirements.txt
# or, if you use poetry/pyproject later:
# pip install .
```

### 4) Configure secrets
Create `.env` in the project root:
```dotenv
# LLM backends
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...

# Speech / TTS (optional)
SPEECH_RECOGNITION_DEVICE=default
TTS_VOICE=auto
```

If you prefer YAML, create `config.yaml`:
```yaml
llm:
  provider: openai  # or 'anthropic'
  model: gpt-4o     # adjust as needed
  temperature: 0.2
keys:
  openai:    "${ env.OPENAI_API_KEY }"
  anthropic: "${ env.ANTHROPIC_API_KEY }"
audio:
  enable_stt: true
  enable_tts: false
```

> The app will read `.env` first; `config.yaml` can override specific settings if present.

---

## ▶️ Run the Streamlit app

```bash
streamlit run src/app/hyri_streamlit_app.py
```

**CLI (example)**:
```bash
python src/HiRI.py --mode chat --provider openai --model gpt-4o
```

---

## 🧩 Features

- **LLM abstraction** (OpenAI/Anthropic).  
- **Speech recognition** via `speech_recognition`.  
- **Text-to-speech** via `pyttsx3`.  
- **Data utilities** with `pandas`.  
- **Web UI** via Streamlit.  

---

## 🗂️ Repository layout

```
src/
  app/
    hyri_streamlit_app.py   # Streamlit UI
  HiRI.py                   # CLI entrypoint (example)
docs/
  neuroglyph_platform_guide.md
```

---

## 🧪 Testing

```bash
pip install -U pip pytest pytest-cov
pytest -q
```

---

## 🛠️ Development

- Code style: `black`, `ruff`, `isort`  
- Types: `mypy` (optional)  
- Pre-commit: add `.pre-commit-config.yaml` and hooks

---

## 🗺️ Roadmap

- [ ] Package `pyproject.toml` and publish internal wheels
- [ ] Add unit + integration tests
- [ ] Modular skill registry (STT/TTS/tools)
- [ ] Session logging + analytics
- [ ] Dockerfile + `docker-compose`

---

## 🤝 Contributing

PRs welcome. Please open an issue first for major changes. Add tests for new features.

---

## 📄 License

Apache-2.0 (proposed).

---

## 📚 Citation

If you use HyRI in research, please cite:
```bibtex
@misc{{hyri2025,
  title={{HyRI}: Hybrid Relational Intelligence},
  year={2025},
  howpublished={{GitHub} repository}
}}
```
