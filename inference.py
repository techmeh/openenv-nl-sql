import asyncio
import os
import re
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI

from models import NlSqlAnalyticsAction
from server.nl_sql_analytics_env_environment import (
    NlSqlAnalyticsEnvironment,
)

# ======================
# Environment Variables
# ======================

API_KEY = os.getenv("HF_TOKEN")

API_BASE_URL = (
    os.getenv("API_BASE_URL")
    or "https://router.huggingface.co/v1"
)

MODEL_NAME = (
    os.getenv("MODEL_NAME")
    or "Qwen/Qwen2.5-7B-Instruct"
)

BENCHMARK = "nl_sql_analytics_env"

MAX_STEPS = 5

SUCCESS_SCORE_THRESHOLD = 0.8


# ======================
# Logging Functions
# ======================

def log_start(task: str, env: str, model: str):
    print(
        f"[START] task={task} env={env} model={model}",
        flush=True,
    )


def log_step(
    step: int,
    action: str,
    reward: float,
    done: bool,
    error: Optional[str],
):

    error_val = error if error else "null"
    done_val = str(done).lower()

    print(
        f"[STEP] step={step} action={action} "
        f"reward={reward:.2f} "
        f"done={done_val} "
        f"error={error_val}",
        flush=True,
    )


def log_end(
    success: bool,
    steps: int,
    score: float,
    rewards: List[float],
):

    rewards_str = ",".join(
        f"{r:.2f}" for r in rewards
    )

    print(
        f"[END] success={str(success).lower()} "
        f"steps={steps} "
        f"score={score:.3f} "
        f"rewards={rewards_str}",
        flush=True,
    )


# ======================
# SQL Cleanup
# ======================

def clean_sql(sql: str) -> str:

    sql = sql.strip()

    # Remove markdown
    sql = re.sub(
        r"```sql|```",
        "",
        sql,
        flags=re.IGNORECASE,
    )

    # Remove SQL: prefix
    sql = re.sub(
        r"^SQL\s*:\s*",
        "",
        sql,
        flags=re.IGNORECASE,
    )

    # Remove aliases (AS something)
    sql = re.sub(
        r"\s+AS\s+\w+",
        "",
        sql,
        flags=re.IGNORECASE,
    )

    return sql.strip()


# ======================
# SQL Generation
# ======================

SYSTEM_PROMPT = """
You are an expert SQLite SQL generator.

Return ONLY SQL.
No markdown.
No explanations.
No aliases.
Never use AS.

Schema:

customers(
    id INTEGER,
    name TEXT,
    city TEXT
)

orders(
    customer_id INTEGER,
    amount REAL
)

Examples:

Question:
Show all customer names
SQL:
SELECT name FROM customers

Question:
List all customers from Chennai
SQL:
SELECT * FROM customers WHERE city = 'Chennai'

Question:
Find total order amount per customer
SQL:
SELECT customer_id, SUM(amount)
FROM orders
GROUP BY customer_id
"""


def generate_sql(
    client,
    question: str,
    previous_error: Optional[str] = None,
):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    if previous_error:

        messages.append(
            {
                "role": "assistant",
                "content": previous_error,
            }
        )

    try:

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.0,
            max_tokens=120,
        )

        sql = (
            completion
            .choices[0]
            .message
            .content
        )

        return clean_sql(sql)

    except Exception as e:

        print(f"[DEBUG] LLM Error: {e}")

        return "SELECT * FROM customers LIMIT 1"


# ======================
# Main Execution
# ======================

async def main():

    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY,
    )

    env = NlSqlAnalyticsEnvironment()

    rewards = []
    steps_taken = 0
    success = False
    score = 0.0

    previous_feedback = None

    try:

        # ✅ RESET ONLY ONCE
        obs = env.reset()

        # ✅ Get task from environment
        task_name = env.state["task"]["task"]

        # Log start
        log_start(
            task=task_name,
            env=BENCHMARK,
            model=MODEL_NAME,
        )

        # Get question
        question = obs.message

        print(
            f"[QUESTION] {question}",
            flush=True,
        )

        done = False

        # ======================
        # Agent Loop
        # ======================

        for step in range(1, MAX_STEPS + 1):

            sql_query = generate_sql(
                client,
                question,
                previous_feedback,
            )

            obs = env.step(
                NlSqlAnalyticsAction(
                    question=question,
                    sql_query=sql_query,
                )
            )

            reward = obs.reward or 0.0
            done = obs.done

            rewards.append(reward)

            steps_taken = step

            previous_feedback = obs.message

            log_step(
                step=step,
                action=sql_query,
                reward=reward,
                done=done,
                error=None,
            )

            if done:
                break

        score = (
            sum(rewards) / len(rewards)
            if rewards
            else 0.0
        )

        success = done

    finally:

        try:
            if hasattr(env, "close"):
                env.close()
        except Exception:
            pass

        log_end(
            success=success,
            steps=steps_taken,
            score=score,
            rewards=rewards,
        )


if __name__ == "__main__":
    asyncio.run(main())