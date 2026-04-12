from uuid import uuid4
from typing import Optional

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from models import (
    NlSqlAnalyticsAction,
    NlSqlAnalyticsObservation
)


class NlSqlAnalyticsEnvironment(Environment):
    """
    SQL Analytics Environment
    """

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self._state = State(
            episode_id=str(uuid4()),
            step_count=0
        )

        self._reset_count = 0
        self._current_task = None

        self.tasks = [
            {
                "task": "nl_sql_query",
                "question": "Show all customer names",
                "expected_sql": "SELECT name FROM customers"
            },
            {
                "task": "customer_lookup",
                "question": "Find customer with ID 123",
                "expected_sql": "SELECT * FROM customers WHERE id = 123"
            },
            {
                "task": "sales_summary",
                "question": "Summarize total sales",
                "expected_sql": "SELECT SUM(amount) FROM sales"
            }
        ]

    # RESET
    def reset(self, task_name: Optional[str] = None) -> NlSqlAnalyticsObservation:

        self._state = State(
            episode_id=str(uuid4()),
            step_count=0
        )

        self._reset_count += 1

        if task_name is None:
            task_name = "nl_sql_query"

        selected_task = next(
            (t for t in self.tasks if t["task"] == task_name),
            None
        )

        if selected_task is None:
            raise ValueError(f"Invalid task: {task_name}")

        self._current_task = selected_task

        return NlSqlAnalyticsObservation(
            result=None,
            correct=False,
            message=selected_task["question"],
            reward=0.5,
            done=False
        )

    # STEP
    def step(self, action) -> NlSqlAnalyticsObservation:

        if self._current_task is None:
            return NlSqlAnalyticsObservation(
                result=None,
                correct=False,
                message="Environment not reset.",
                reward=0,
                done=False
            )

        if isinstance(action, dict):
            predicted_sql = action.get("sql_query", "")
        else:
            predicted_sql = getattr(action, "sql_query", "")

        expected_sql = self._current_task["expected_sql"]

        correct = predicted_sql.strip().upper() == expected_sql.strip().upper()

        reward = 0.91 if correct else 0.12  # MUST be (0,1)

        self._state.step_count += 1

        return NlSqlAnalyticsObservation(
            result=None,
            correct=correct,
            message="Evaluation complete",
            reward=reward,
            done=correct
        )

    # STATE (STRICT OFFICIAL STYLE)
    @property
    def state(self) -> State:
        """
        Return current environment state.
        MUST return openenv State object.
        """
        return self._state
