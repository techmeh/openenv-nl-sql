def grade(action, observation):
    if action.get("sql_query") and observation.get("correct"):
        return {"score": 1, "message": "Valid output"}
    return {"score": 0, "message": "Invalid or missing output"}
