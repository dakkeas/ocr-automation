import requests
import json
import os
import time
from abbyy_auth import get_access_token
from dotenv import load_dotenv

# Load all environment variables defined in the local `.env` file into `os.environ`.
# This is crucial for securely injecting credentials without hardcoding them.
load_dotenv()

# =========================================================================================
# --- CONFIGURATION LAYER ---
# =========================================================================================
# TENANT_ID: Your unique ABBYY Tenant identifier (e.g. your workspace space).
# SKILL_ID: The unique identifier for the specific Machine Learning model or "Skill" you want to use.
# BASE_URL: The host URL for the API. In this case, 'vantage-au.abbyy.com' for the Australia server.
# FILE_PATH: The local path to the document you wish to upload and process.

TENANT_ID = os.environ.get("ABBYY_TENANT_ID")
SKILL_ID = "4cf33492-adb5-43e5-b8c7-0a9a146886da"
BASE_URL = "https://vantage-au.abbyy.com/api/publicapi/v1"
FILE_PATH = "test_data.pdf"


def process_document(access_token):
    """
    Main pipeline function that orchestrates the ABBYY OCR lifecycle.
    
    The ABBYY Vantage Multi-Step API requires creating an empty transaction, uploading 
    files to it, formally starting the "process", and polling for asynchronous completion.
    
    Args:
        access_token (str): The OAuth2 Bearer token required for API authorization.
    """
    if not access_token:
        print("No access token provided. Aborting process.")
        return

    # Base headers required for API communication.
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # =========================================================================================
    # LAYER 1: CREATING THE TRANSACTION
    # =========================================================================================
    # Before uploading any files, we must create an empty "Transaction" envelope and tell 
    # ABBYY which Skill (OCR model) it should use to process the documents placed inside.
    print(f"1. Creating transaction for Skill ID: {SKILL_ID}...")
    create_url = f"{BASE_URL}/transactions"
    payload = {
        "SkillId": SKILL_ID
    }
    
    response = requests.post(create_url, headers=headers, json=payload)
    if response.status_code not in [200, 201]:
        print(f"Failed to create transaction: {response.status_code}")
        print(response.text)
        return

    # Parse the response to extract the new Transaction ID. 
    # Fallback to 'id' if 'transactionId' key is not present (due to API version differences).
    data = response.json()
    transaction_id = data.get("transactionId")
    if not transaction_id:
        transaction_id = data.get("id")
        
    if not transaction_id:
        print(f"Failed to extract transaction ID from response: {data}")
        return
        
    print(f"Transaction ID: {transaction_id}")

    # =========================================================================================
    # LAYER 2: UPLOADING THE DOCUMENT
    # =========================================================================================
    # Once the transaction exists, we upload the actual file logic bytes to it.
    print(f"2. Uploading {FILE_PATH}...")
    upload_url = f"{BASE_URL}/transactions/{transaction_id}/files"
    
    # NOTE: When sending `multipart/form-data` using requests.post(files=...), 
    # Python's `requests` library will automatically generate the `Content-Type` boundary.
    # Passing our original `headers` which contains `Content-Type: application/json` will break the upload.
    # Therefore, we only pass the Authorization token for this specific request.
    upload_headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    with open(FILE_PATH, "rb") as f:
        # Structure the payload as a file tuple: (filename, file_object, mime_type)
        files = {
            "file": (os.path.basename(FILE_PATH), f, "application/pdf")
        }
        # Send the binary payload.
        upload_response = requests.post(upload_url, headers=upload_headers, files=files)

    if upload_response.status_code not in [200, 201]:
        print(f"Failed to upload file: {upload_response.status_code}")
        print(upload_response.text)
        return
    print("Upload successful.")

    # =========================================================================================
    # LAYER 3: STARTING THE PROCESSING
    # =========================================================================================
    # Uploading the files does not automatically trigger OCR. 
    # We must hit the `/start` endpoint to move the transaction into the ABBYY execution queue.
    print("3. Starting processing...")
    process_url = f"{BASE_URL}/transactions/{transaction_id}/start"
    process_response = requests.post(process_url, headers=headers)
    
    if process_response.status_code not in [200, 202, 204]:
        print(f"Failed to start processing: {process_response.status_code}")
        print(process_response.text)
        return
    print("Processing started.")

    # =========================================================================================
    # LAYER 4: ASYNCHRONOUS POLLING (WAITING FOR RESULTS)
    # =========================================================================================
    # OCR can take seconds or minutes depending on the load and page count. 
    # We continuously ping the transaction status endpoint until it reaches a terminal state.
    print("4. Polling for status...")
    status_url = f"{BASE_URL}/transactions/{transaction_id}"
    
    while True:
        status_response = requests.get(status_url, headers=headers)
        if status_response.status_code != 200:
            print(f"Error checking status: {status_response.status_code}")
            break
            
        data = status_response.json()
        status = data.get("status")
        
        # Output the exact payload from the server so we can monitor metadata shifts in real-time.
        print("\n--- Current Transaction Status ---")
        print(json.dumps(data, indent=2))
        
        # Terminal success states: we are ready to proceed to file downloading.
        if status in ["Processed", "ProcessedWithWarnings"]:
            print("Processing complete!")
            break
            
        # Blocking states: The AI is unconfident and requires a human to verify fields in the UI.
        elif status in ["Exception", "ManualReview", "RequiresReview"]:
            print(f"\nDocument requires manual review or has an exception (Status: {status}).")
            print("Transaction Details:")
            print(json.dumps(data, indent=2))
            print("\nPlease complete the review in the ABBYY Vantage UI and run a retrieval script later.")
            return
            
        # Terminal failure states: System failure or human deletion.
        elif status in ["NotProcessed", "Deleted"]:
            print(f"Processing failed with status: {status}")
            print("Transaction Details:")
            print(json.dumps(data, indent=2))
            return
            
        # Pause for 5 seconds before hitting the server again to avoid Rate Limiting.
        time.sleep(5)

    # =========================================================================================
    # LAYER 5: DOWNLOADING ALL EXPORT FORMATS
    # =========================================================================================
    # At this stage, ABBYY has generated the extracted data according to the Skill's Export Settings.
    print("5. Successfully processed. Fetching result files...")
    
    # Retrieve the document object which houses our resulting artifacts.
    documents = data.get("documents", [])
    if not documents:
        print("No documents found in result.")
        return
        
    # The 'resultFiles' array contains metadata for every file format ABBYY was told to export (CSV, JSON, XML, etc.)
    result_files = documents[0].get("resultFiles", [])
    if not result_files:
        print("No result files found. Make sure your skill has export settings configured.")
        return
        
    print(f"Found {len(result_files)} result file(s). Downloading...")
    
    # Iterate through every export format available and download them systematically.
    
    # Create the output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate a timestamp to attach to the filenames
    timestamp_str = time.strftime("%Y%m%d_%H%M%S")
    
    for rf in result_files:
        # Extract the backend fileId and the human-readable filename designated by the Skill.
        file_id = rf.get("fileId")
        original_file_name = rf.get("fileName", f"result_{file_id}")
        
        # Attach the timestamp and path
        file_name = f"{timestamp_str}_{original_file_name}"
        file_path = os.path.join(output_dir, file_name)
        
        print(f"Downloading {original_file_name} to {file_path} (File ID: {file_id})...")
        download_url = f"{BASE_URL}/transactions/{transaction_id}/files/{file_id}/download"
        download_response = requests.get(download_url, headers=headers)
        
        if download_response.status_code == 200:
            # If it's a JSON file, parse it as a dictionary and write it beautifully with indentation.
            if original_file_name.endswith(".json"):
                result_content = download_response.json()
                print(f"\n--- {original_file_name} DATA ---")
                print(json.dumps(result_content, indent=4))
                with open(file_path, "w") as f:
                    json.dump(result_content, f, indent=4)
            else:
                # If it's a CSV, PDF, or XML, write the raw binary content precisely as it arrived.
                with open(file_path, "wb") as f:
                    f.write(download_response.content)
            print(f"Saved to {file_path}")
        else:
            print(f"Failed to download {original_file_name}: {download_response.status_code}")

if __name__ == "__main__":
    # Orchestrator block: acquire the token using credentials, then run the pipeline.
    token = get_access_token()
    if token:
        process_document(token)

