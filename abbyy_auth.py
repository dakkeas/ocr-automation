import requests
import os
from dotenv import load_dotenv

# Load credentials from .env if it exists
load_dotenv()

# --- 1. SETTING UP ---
# Using the values from your original token.py script
# It's better to store these in the .env file later!
MY_EMAIL = os.environ.get("ABBYY_EMAIL")
MY_PASSWORD = os.environ.get("ABBYY_PASSWORD")
MY_CLIENT_ID = os.environ.get("ABBYY_CLIENT_ID")
MY_CLIENT_SECRET = os.environ.get("ABBYY_CLIENT_SECRET")
MY_TENANT_ID = os.environ.get("ABBYY_TENANT_ID")

def get_access_token():
    # --- 2. THE LOGIC ---
    # Using the AU endpoint based on your previous URL
    url = f"https://vantage-au.abbyy.com/auth2/{MY_TENANT_ID}/connect/token"

    payload = {
        'grant_type': 'password',
        'scope': 'openid permissions global.wildcard',
        'username': MY_EMAIL,
        'password': MY_PASSWORD,
        'client_id': MY_CLIENT_ID,
        'client_secret': MY_CLIENT_SECRET
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        print(f"Requesting token from Tenant {MY_TENANT_ID}...")
        response = requests.post(url, data=payload, headers=headers)
        
        # Raise an exception if the request failed
        response.raise_for_status()
        
        token_data = response.json()
        access_token = token_data.get("access_token")
        
        return access_token

    except requests.exceptions.HTTPError as err:
        print(f"\nFAILED! The Server said: {err}")
        print(response.text)
        return None
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        return None

if __name__ == "__main__":
    token = get_access_token()
    if token:
        print("\nSUCCESS! Here is your Access Token:")
        print(token)
