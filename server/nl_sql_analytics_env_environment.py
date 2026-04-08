# nl_sql_analytics_env_environment.py
from typing import Optional
from uuid import uuid4

from openenv.core.env_server.types import (
    ResetResponse,
    StepResponse,
)
from openenv.core.env_server import Environment
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from models import NlSqlAnalyticsState, NlSqlAnalyticsAction, NlSqlAnalyticsObservation


class NlSqlAnalyticsEnvironment(Environment):
    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self):
        super().__init__()
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

    def reset(self, task_name: Optional[str] = None):
        print("RESET CALLED")
        print("Task received:", task_name)

        if task_name is None:
            task_name = "nl_sql_query"

        # Select the task
        selected_task = next((t for t in self.tasks if t["task"] == task_name), None)
        if selected_task is None:
            raise ValueError(f"Invalid task name: {task_name}")

        # Initialize state
        self.state = NlSqlAnalyticsState(
            task=selected_task["task"],
            expected_sql=selected_task["expected_sql"],
            step_count=0
        )
        self.done = False

        print("Selected task:", self.state.task)
        print("Expected SQL:", self.state.expected_sql)

        # Create observation
        observation = NlSqlAnalyticsObservation(
            result=None,
            correct=False,
            message=selected_task["question"],
            reward=0.0,
            done=False
        )

        # Save last observation
        self.last_observation = observation

        # Return serialized observation (dictionary) only
        return ResetResponse(observation=observation.model_dump())

    def step(self, action: NlSqlAnalyticsAction):
        print("STEP CALLED")
        current_task = getattr(self.state, "task", None)
        expected_sql = getattr(self.state, "expected_sql", None)
        print("Current task:", current_task)

        if current_task is None:
            observation = NlSqlAnalyticsObservation(
                result=None,
                correct=False,
                message="Environment not reset. Call /reset first.",
                reward=0.0,
                done=False
            )
            self.last_observation = observation
            return StepResponse(observation=observation.model_dump())

        # Compare predicted SQL
        predicted_sql = action.sql_query
        correct = predicted_sql.strip().lower() == expected_sql.strip().lower()
        reward = 1.0 if correct else 0.0

        # Create observation
        observation = NlSqlAnalyticsObservation(
            result=None,
            correct=correct,
            message="Evaluation complete",
            reward=reward,
            done=True
        )

        self.last_observation = observation
        self.done = True

        return StepResponse(observation=observation.model_dump())
    
    def state(self) -> NlSqlAnalyticsObservation:
        """
        Returns the current environment observation in the required format.
        """
        # If you already keep the latest observation in self._obs:
        return self._obs