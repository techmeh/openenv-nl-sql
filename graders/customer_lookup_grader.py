def grade(task, prediction, reference, observation):

    predicted = prediction.get("sql_query", "")

    expected_sql = "SELECT * FROM customers WHERE id = 123"

    if predicted.lower().strip() == expected_sql.lower().strip():
        return 0.88

    return 0.15
