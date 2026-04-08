from openenv.core.env_client import EnvClient
from openenv.core.sync_client import SyncEnvClient

from models import NlSqlAnalyticsAction
from server.nl_sql_analytics_env_environment import (
    NlSqlAnalyticsEnvironment,
)


def main():

    # Create async client
    async_client = EnvClient(
        env_class=NlSqlAnalyticsEnvironment
    )

    # Wrap into sync client
    client = SyncEnvClient(async_client)

    # Reset environment
    obs = client.reset()

    print("\nQUESTION:")
    print(obs.message)

    # Send SQL attempt
    action = NlSqlAnalyticsAction(
        question=obs.message,
        sql_query="SELECT name FROM customers"
    )

    obs = client.step(action)

    print("\nRESULT:")
    print(obs.result)

    print("\nCORRECT:")
    print(obs.correct)

    print("\nMESSAGE:")
    print(obs.message)


if __name__ == "__main__":
    main()