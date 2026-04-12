# import requests

# BASE = "http://127.0.0.1:8000"

# # Reset environment
# resp = requests.post(f"{BASE}/reset")
# reset_data = resp.json()
# observation = reset_data["observation"]
# print("Observation after reset:", observation)

# # Step environment
# step_payload = {
#     "action": {
#         "question": "Show all customer names",
#         "sql_query": "SELECT name FROM customers"  # optional, depending on your env
#     }
# }
# resp2 = requests.post(f"{BASE}/step", json=step_payload)

# # Debugging if JSON fails
# print("Status code:", resp2.status_code)
# print("Raw response:", resp2.text)

# if resp2.status_code == 200:
#     step_data = resp2.json()
#     print("Step response:", step_data)

# from graders.nl_sql_query_grader import grade

# action = {
#     "sql_query": "SELECT name FROM customers"
# }

# observation = {}

# result = grade(action, observation)

# print(result)

import importlib
import inspect
import yaml
import os
import sys


# =========================
# CONFIG
# =========================
YAML_PATH = "openenv.yaml"


# =========================
# UTIL
# =========================
def fail(msg):
    print(f" FAIL: {msg}")
    sys.exit(1)


def ok(msg):
    print(f"✅ {msg}")


# =========================
# LOAD YAML
# =========================
if not os.path.exists(YAML_PATH):
    fail("openenv.yaml not found")

with open(YAML_PATH, "r") as f:
    config = yaml.safe_load(f)


tasks = config.get("tasks", [])


# =========================
# CHECK TASK COUNT
# =========================
if len(tasks) < 3:
    fail(f"Need at least 3 tasks, found {len(tasks)}")

ok(f"{len(tasks)} tasks found")


# =========================
# CHECK GRADERS
# =========================

for task in tasks:
    name = task["name"]
    grader_path = task.get("grader")

    if not grader_path:
        fail(f"Task '{name}' missing grader")

    if "." not in grader_path:
        fail(f"Invalid grader path '{grader_path}' (must include .grade)")

    module_name, func_name = grader_path.rsplit(".", 1)

    try:
        module = importlib.import_module(module_name)
    except Exception as e:
        fail(f"Cannot import grader module '{module_name}': {e}")

    if not hasattr(module, func_name):
        fail(f"Missing function '{func_name}' in {module_name}")

    grade_fn = getattr(module, func_name)

    if not callable(grade_fn):
        fail(f"{grader_path} is not callable")

    ok(f"Loaded {grader_path}")


# =========================
# TEST GRADER OUTPUT
# =========================

dummy_action = {"sql_query": "SELECT name FROM customers"}
dummy_obs = {"correct": True}

for task in tasks:
    module_name, func_name = task["grader"].rsplit(".", 1)
    module = importlib.import_module(module_name)
    grade_fn = getattr(module, func_name)

    try:
        result = grade_fn(
            task["name"],
            dummy_action,
            None,
            dummy_obs
        )
    except Exception as e:
        fail(f"Grader crash in {task['name']}: {e}")

    # must be float
    if not isinstance(result, (float, int)):
        fail(f"{task['name']} returns NON-FLOAT: {type(result)}")

    # must be in range
    if result <= 0 or result >= 1:
        fail(f"{task['name']} score out of range: {result}")

    ok(f"{task['name']} → score {result}")


# =========================
# FINAL PASS
# =========================
print(" ALL CHECKS PASSED — READY TO SUBMIT!")
