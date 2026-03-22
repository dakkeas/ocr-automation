# Run this separately with your generated Transaction ID

import requests
import json
from abbyy_auth import get_access_token

token = get_access_token()
headers = {"Authorization": f"Bearer {token}"}
test_url = f"https://vantage-au.abbyy.com/api/publicapi/v1/transactions/6352f22a-f15d-4301-b601-a460004a77e1"
res = requests.get(test_url, headers=headers)
print(json.dumps(res.json(), indent=2))