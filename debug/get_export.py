import requests
import json
import os
from abbyy_auth import get_access_token

# --- CONFIGURATION ---
SKILL_ID = os.environ.get("ABBYY_SKILL_ID")
BASE_URL = "https://vantage-au.abbyy.com/api/publicapi/v1"

def download_all_finished_exports(access_token):
    if not access_token:
        return

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # 1. Get a list of transactions. 
    # Increased Limit to 50 to catch more "finished" jobs.
    list_url = f"{BASE_URL}/transactions?SkillId={SKILL_ID}&Limit=50"
    
    print(f"Fetching transactions for Skill: {SKILL_ID}...")
    response = requests.get(list_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to list transactions: {response.status_code}\n{response.text}")
        return

    data = response.json()
    transactions = data.get("items", [])

    if not transactions:
        print("No transactions found.")
        return

    print(f"Found {len(transactions)} total transactions. Filtering for 'Completed'...")

    for tx in transactions:
        tx_id = tx['id']
        status = tx.get('status')

        # We only care about Completed jobs
        if status != "Completed":
            print(f"Skipping TX {tx_id} (Status: {status})")
            continue

        print(f"\n--- Processing Transaction: {tx_id} ---")

        # 2. Get the full detail for this specific transaction
        detail_url = f"{BASE_URL}/transactions/{tx_id}"
        detail_res = requests.get(detail_url, headers=headers)
        
        if detail_res.status_code != 200:
            print(f"Could not get details for {tx_id}")
            continue
        
        full_tx = detail_res.json()
        documents = full_tx.get('documents', [])
        
        # 3. Find and Download JSON files
        for doc in documents:
            result_files = doc.get('resultFiles', [])
            for r_file in result_files:
                if r_file.get('name', '').lower().endswith('.json'):
                    file_id = r_file['id']
                    file_name = r_file['name']
                    
                    # Download
                    dl_url = f"{BASE_URL}/transactions/{tx_id}/files/{file_id}/download"
                    dl_res = requests.get(dl_url, headers=headers)
                    
                    if dl_res.status_code == 200:
                        # Save to a local file so they don't just scroll past in the terminal
                        local_filename = f"export_{tx_id}.json"
                        with open(local_filename, 'w') as f:
                            json.dump(dl_res.json(), f, indent=4)
                        print(f"Successfully saved export to {local_filename}")
                    else:
                        print(f"Failed to download {file_name}")

if __name__ == "__main__":
    token = get_access_token()
    if token:
        download_all_finished_exports(token)