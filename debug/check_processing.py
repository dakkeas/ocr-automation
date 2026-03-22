import requests
from abbyy_auth import get_access_token

token = get_access_token()
headers = {"Authorization": f"Bearer {token}"}

url = "https://vantage-au.abbyy.com/api/publicapi/v1/processing/transactions"
print(f"Testing {url}...")
try:
    r = requests.post(url, headers=headers, json={"SkillId": "b5745e21-65f6-4a92-895e-cfabd6c40ee4"})
    print(f"POST Status: {r.status_code}")
    print(f"POST Body: {r.text}")
except Exception as e:
    print(f"Error: {e}")
