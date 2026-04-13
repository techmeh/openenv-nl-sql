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

Validation steps
malav@MyBook MINGW64 ~
$ curl -X POST https://malavikad25-openenv-nl-sql-converter.hf.space/reset -H "X-Session-Id: 123"
{"observation":{"result":null,"correct":false,"message":"Show all customer names"},"reward":0.1,"done":false}
malav@MyBook MINGW64 ~
$ curl -X POST https://malavikad25-openenv-nl-sql-converter.hf.space/step -H "Content-Type: application/json" -d '{"action": {"sql_query": "SELECT name FROM customers"}}' -H "X-Session-Id: 123"
{"observation":{"result":null,"correct":true,"message":"Evaluation complete"},"reward":0.9,"done":true}
malav@MyBook MINGW64 ~
$ curl https://malavikad25-openenv-nl-sql-converter.hf.space/health             {"status":"healthy"}
malav@MyBook MINGW64 ~
$ curl https://malavikad25-openenv-nl-sql-converter.hf.space/state              {"episode_id":"72abff6a-13e7-4c8c-8d1d-0ab8ba983e74","step_count":1}
