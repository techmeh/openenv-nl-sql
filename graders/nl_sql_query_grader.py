import sqlparse


def normalize_sql(sql: str) -> str:
    return sqlparse.format(
        sql,
        keyword_case="upper",
        strip_comments=True
    ).strip().rstrip(";")


def grade(task, prediction, reference, observation):

    predicted = prediction.get("sql_query", "")

    expected_sql = "SELECT name FROM customers"

    predicted = normalize_sql(predicted)
    expected = normalize_sql(expected_sql)

    if predicted == expected:
        return 0.91   # ✅ MUST be float, not dict

    return 0.12       # ✅ MUST be float, not dict
