def grade(action, observation):

    predicted = action.get("sql_query", "")

    expected_sql = "SELECT * FROM customers WHERE id = 123"

    if predicted.lower().strip() == expected_sql.lower().strip():

        return {
            "score": 0.85,
            "message": "Correct lookup query"
        }

    return {
        "score": 0.3,
        "message": "Incorrect lookup query"
    }