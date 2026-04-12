from pydantic import BaseModel
from typing import Optional


# STATE
class NlSqlAnalyticsState(BaseModel):

    task: str
    expected_sql: str
    step_count: int = 0


# ACTION
class NlSqlAnalyticsAction(BaseModel):

    sql_query: str


class NlSqlAnalyticsObservation(BaseModel):

    result: Optional[str] = None
    correct: bool
    message: str

    reward: float
    done: bool
