---
title: Openenv Nl Sql Converter
emoji: 🐢
colorFrom: yellow
colorTo: gray
sdk: docker
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

---
title: Openenv Nl Sql Converter
emoji: 🐢
colorFrom: yellow
colorTo: gray
sdk: docker
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference


# NL-SQL Analytics Environment — OpenEnv Submission

## Overview
`nl_sql_analytics_env` is a **Natural Language to SQL environment** for AI agents.  
It allows agents to interact with a simulated analytics environment where natural language questions are converted into SQL queries and executed on a sample database.  

The environment is:
- **Dockerized** for HF Space deployment.
- **Validator-ready** with `/reset` endpoint.
- Compatible with **OpenEnv multi-mode deployment**.

---

## Architecture & Concept
+---------------------+ +--------------------+
| AI Agent / LLM | <---> | OpenEnv NL-SQL Env |
| (queries in NL) | | - reset() |
| | | - step(action) |
+---------------------+ +---------+----------+
|
v
+--------------------+
| Simulated Database |
| (SQLite / in-memory) |
+--------------------+


- **AI Agent / LLM** sends natural language questions like “Show all customer names”.
- **OpenEnv environment** receives actions (SQL queries) and maintains state, reward, and observations.
- **Simulated database** executes SQL and returns results.
- **FastAPI `/reset` endpoint** allows external systems (e.g., validator, HF Space) to reset the environment state.

---

## How OpenEnv is Used
- `NlSqlAnalyticsEnv` implements the **OpenEnv spec** with typed models:  
  - `reset()` → initializes environment and returns the initial state.  
  - `step(action)` → executes SQL action and returns `(observation, reward, done, info)`.  
- OpenEnv **enables multi-mode interaction**: the same environment can be used locally, in Docker, or in HF Space.  
- Validator uses `/reset` and multi-step interactions to ensure your environment behaves as expected.

---

## Setup & Run

**Local (venv):**
```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
pip install -r requirements.txt
python app.py
curl -X POST http://127.0.0.1:7860/reset
