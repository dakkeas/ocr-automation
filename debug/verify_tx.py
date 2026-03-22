import requests
from abbyy_auth import get_access_token

token = get_access_token()
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
skill_id = "4cf33492-adb5-43e5-b8c7-0a9a146886da"

url = "https://vantage-au.abbyy.com/api/publicapi/v1/transactions"
print(f"Creating transaction at {url}...")
r = requests.post(url, headers=headers, json={"SkillId": skill_id})
print(f"Status: {r.status_code}")
print(f"Body: {r.text}")
if r.status_code in [200, 201]:
    tx_id = r.json().get("id")
    print(f"SUCCESS! Transaction ID: {tx_id}")
