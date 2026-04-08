from server.nl_sql_analytics_env_environment import (
    NlSqlAnalyticsEnvironment,
)

from models import NlSqlAnalyticsAction


env = NlSqlAnalyticsEnvironment()

# Reset
obs = env.reset()

print("\nQUESTION:")
print(obs.message)

# Step
action = NlSqlAnalyticsAction(
    question=obs.message,
    sql_query="SELECT name FROM customers"
)

obs = env.step(action)

print("\nRESULT:")
print(obs.result)

print("\nCORRECT:")
print(obs.correct)

print("\nMESSAGE:")
print(obs.message)