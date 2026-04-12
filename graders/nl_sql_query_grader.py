def grade(task, prediction, reference, observation):

    predicted = prediction.get("sql_query", "")

    expected = "SELECT name FROM customers"

    if predicted.strip().lower() == expected.lower():
        return 0.91

    return 0.12
