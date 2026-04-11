def grade(action, observation):

    predicted = action.get("sql_query", "")

    expected_sql = "SELECT SUM(amount) FROM sales"

    if predicted.lower().strip() == expected_sql.lower().strip():

        return {
            "score": 0.8,
            "message": "Correct aggregation query"
        }

    return {
        "score": 0.25,
        "message": "Incorrect aggregation query"
    }