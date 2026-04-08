import requests

BASE = "http://127.0.0.1:8000"

# Reset environment
resp = requests.post(f"{BASE}/reset")
reset_data = resp.json()
observation = reset_data["observation"]
print("Observation after reset:", observation)

# Step environment
step_payload = {
    "action": {
        "question": "Show all customer names",
        "sql_query": "SELECT name FROM customers"  # optional, depending on your env
    }
}
resp2 = requests.post(f"{BASE}/step", json=step_payload)

# Debugging if JSON fails
print("Status code:", resp2.status_code)
print("Raw response:", resp2.text)

if resp2.status_code == 200:
    step_data = resp2.json()
    print("Step response:", step_data)