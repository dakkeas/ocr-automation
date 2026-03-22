ABBYY Vantage Document Processor


Follow these steps to set up and run the document processor.

1. Configuration (.env)
Create a file named .env in the root directory. This file is ignored by Git to keep your credentials secure. Add your ABBYY Vantage details as follows:

Code snippet
ABBYY_TENANT_ID=your_tenant_id_here
ABBYY_CLIENT_ID=your_client_id_here
ABBYY_CLIENT_SECRET=your_client_secret_here
ABBYY_USERNAME=your_email_here
ABBYY_PASSWORD=your_password_here
ABBYY_SKILL_ID=4cf33492-adb5-43e5-b8c7-0a9a146886da

2. Installation
Ensure you have Python installed, then install the required dependencies:

pip install -r requirements.txt

3. Prepare Ingestion
Place all the documents you want to process (PDFs, Images, etc.) into the folder named files.

mkdir files

# Move your documents into the /files directory

4. Run the Processor
Execute the main script to start the transaction, upload your files, and begin the OCR extraction:


python process_document.py


Manual Review Flow
Currently, this Skill is configured for Manual Review.

Once the AI finishes initial extraction, the terminal will display a Manual Review Link.

Copy and paste this link into your browser to verify the data.

Note: The final JSON export will not be downloaded until the manual review is marked as Submitted/Finished in the Vantage portal.

Project Structure
process_document.py: The main logic for uploading and polling.

abbyy_auth.py: Handles OAuth 2.0 token generation.

.env: (Local only) Stores private credentials.

.gitignore: Prevents secrets and temporary files from being pushed to GitHub.