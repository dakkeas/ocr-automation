import requests
import json
from abbyy_auth import get_access_token

token = get_access_token()
headers = {"Authorization": f"Bearer {token}"}

url = "https://vantage-au.abbyy.com/api/publicapi/v1/skills"
r = requests.get(url, headers=headers)
if r.status_code == 200:
    skills = r.json()
    print("Available Skills:")
    for s in skills:
        print(f"ID: {s.get('id')} - Name: {s.get('name')}")
else:
    print(f"Failed to list skills: {r.status_code}")
    print(r.text)
