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