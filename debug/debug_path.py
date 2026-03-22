import requests
from abbyy_auth import get_access_token

token = get_access_token()
headers = {"Authorization": f"Bearer {token}"}

paths = [
    "https://vantage-au.abbyy.com/api/publicapi/v1/skills",
    "https://vantage-au.abbyy.com/api/publicapi/v1/transactions",
    "https://vantage-au.abbyy.com/api/publicapi/v1/processing/transactions",
    "https://vantage-au.abbyy.com/api/publicapi/v1/transactions/launch"
]

for p in paths:
    print(f"Testing {p}...")
    try:
        # For non-GET endpoints, I'll just see if it returns 404 or something else (like 405 or 401)
        r = requests.get(p, headers=headers)
        print(f"GET Status: {r.status_code}")
        
        # Also try POST with empty body (might return 415 or 400 but not 404)
        r_post = requests.post(p, headers=headers, json={})
        print(f"POST Status: {r_post.status_code}")
        
        if r.status_code != 404 or r_post.status_code != 404:
            print(f"Endpoint {p} exists (non-404).")
    except Exception as e:
        print(f"Error: {e}")
