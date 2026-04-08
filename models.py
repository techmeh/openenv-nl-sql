from openenv.core.env_server.types import State, Action, BaseModel
from typing import Optional, Any

class NlSqlAnalyticsState(State):
    task: Optional[str] = None
    expected_sql: Optional[str] = None
    step_count: int = 0
    done: bool = False
    observation: Optional[dict] = None

class NlSqlAnalyticsAction(Action):
    question: str
    sql_query: str

class NlSqlAnalyticsObservation(BaseModel):
    result: Optional[Any] = None
    correct: bool = False
    message: str
    reward: Optional[float] = None
    done: bool = False