def grade(action, observation):
    # Check if SQL query is non-empty and marked correct
    if action.get("sql_query") and observation.get("correct"):
        return {"score": 1, "message": "Valid SQL query"}
    return {"score": 0, "message": "Invalid or missing SQL"}
