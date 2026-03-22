import requests
from abbyy_auth import get_access_token

token = get_access_token()
headers = {"Authorization": f"Bearer {token}"}
skill_id = "b5745e21-65f6-4a92-895e-cfabd6c40ee4"

# 1. Body param
p1 = "https://vantage-au.abbyy.com/api/publicapi/v1/transactions"
print(f"Testing {p1} with SkillId in JSON...")
r1 = requests.post(p1, headers=headers, json={"SkillId": skill_id})
print(f"Status: {r1.status_code}")

# 2. Query param
p2 = "https://vantage-au.abbyy.com/api/publicapi/v1/transactions/launch"
print(f"Testing {p2} with SkillId as query param...")
r2 = requests.post(p2 + f"?SkillId={skill_id}", headers=headers)
print(f"Status: {r2.status_code}")

# 3. List skills check again
p3 = "https://vantage-au.abbyy.com/api/publicapi/v1/skills"
print(f"GET {p3}...")
r3 = requests.get(p3, headers=headers)
print(f"Status: {r3.status_code}")
