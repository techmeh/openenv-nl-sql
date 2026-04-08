import os
import sys
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import uvicorn

print("APP loaded")

try:
    from openenv.core.env_server.http_server import create_app
except Exception as e:
    raise ImportError("openenv is required. Install dependencies first.") from e

# Resolve openenv.yaml relative to repo root
OPENENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "openenv.yaml"))
print("openenv.yaml exists:", os.path.exists(OPENENV_PATH))

from models import NlSqlAnalyticsAction, NlSqlAnalyticsObservation
from server.nl_sql_analytics_env_environment import NlSqlAnalyticsEnvironment

print("Environment import successful")

# Create FastAPI app
app = create_app(
    NlSqlAnalyticsEnvironment,
    NlSqlAnalyticsAction,
    NlSqlAnalyticsObservation,
    env_name="nl_sql_analytics_env",
    max_concurrent_envs=1,
)

# Custom routes
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def root():
    return """
    <h1>NL-SQL Analytics Env</h1>
    <p>Server is running.</p>
    <p>Use API endpoints:</p>
    <ul>
        <li>POST /reset</li>
        <li>POST /step</li>
        <li>GET /state</li>
        <li>GET /schema</li>
    </ul>
    """

@router.get("/health")
def health():
    return {"status": "ok"}

app.include_router(router)

def main():
    port = int(os.environ.get("PORT", 7860))  # Spaces sets PORT dynamically
    uvicorn.run("server.app:app", host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()