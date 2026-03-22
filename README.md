# ABBYY Vantage Document Processor

This project automates document processing using the **ABBYY Vantage Public API (Australia Cluster)**. It handles the full lifecycle of a document: from authentication and upload to status polling and final JSON export.

---

## 🚀 Setup Instructions

### Step 1: Configuration
Create a file named `.env` in the root directory of this project. Add your ABBYY Vantage credentials as follows:

```env
ABBYY_TENANT_ID=5dbc7d5b-059d-4fc5-a2f7-70d588dafaad
ABBYY_CLIENT_ID=your_client_id_here
ABBYY_CLIENT_SECRET=your_client_secret_here
ABBYY_USERNAME=jsantos@medgrocer.com
ABBYY_PASSWORD=your_password_here
ABBYY_SKILL_ID=4cf33492-adb5-43e5-b8c7-0a9a146886da
```

> **Note:** The `.env` file is excluded from Git tracking to keep your credentials secure.

### Step 2: Install Dependencies
Ensure you have Python installed, then run the following command to install the required libraries:

```bash
pip install -r requirements.txt
```

### Step 3: Prepare and Ingest
1. Create a folder named `files` in the project root.
2. Place all documents (PDFs, images) you wish to process into the `files` folder.
3. Run the main processing script:

```bash
python process_document.py
```

### Step 4: Manual Review
This workflow currently triggers a Manual Review evaluation for each document:

1. Once the initial AI extraction is complete, a **Manual Review Link** will be displayed in your terminal.
2. Open this link in your browser to verify or correct the extracted data.
3. **Important:** The script will continue to poll the status and will only download the final results and JSONs once the manual review is marked as Finished/Submitted in the Vantage portal.

---

## 📂 Project Structure

*   `process_document.py` - Main script for batch transaction management, uploading, and polling.
*   `abbyy_auth.py` - Module for handling OAuth 2.0 Bearer Token generation.
*   `.gitignore` - Protects your `.env` and temporary artifacts from being pushed to GitHub.
*   `requirements.txt` - Required python packages.
*   `output/` - A directory automatically generated to store all the downloaded artifact exports cleanly.