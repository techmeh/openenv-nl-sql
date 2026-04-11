import sqlparse


def normalize_sql(sql: str) -> str:
    return sqlparse.format(
        sql,
        keyword_case="upper",
        strip_comments=True
    ).strip().rstrip(";")


def grade(action, observation):

    predicted = action.get("sql_query", "")

    expected_sql = "SELECT name FROM customers"

    predicted = normalize_sql(predicted)
    expected = normalize_sql(expected_sql)

    if predicted == expected:
        return {
            "score": 0.9,
            "message": "Correct SQL"
        }

    return {
        "score": 0.2,
        "message": "Incorrect SQL"
    }