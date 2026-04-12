def grade(task, prediction, reference, observation):

    predicted = prediction.get("sql_query", "")

    expected_sql = "SELECT SUM(amount) FROM sales"

    if predicted.lower().strip() == expected_sql.lower().strip():
        return 0.86

    return 0.14
