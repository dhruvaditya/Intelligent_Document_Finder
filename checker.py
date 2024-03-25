from google.oauth2 import service_account
from googleapiclient.discovery import build
import time

# Set up Google Drive API credentials
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'  

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

# Function to list files in a specific folder
def list_files(folder_id):
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name, modifiedTime)").execute()
    return results.get('files', [])

# Function to check for new files in the folder
def check_for_new_files(folder_id):
    # Get current list of files
    current_files = list_files(folder_id)
    current_file_ids = {file['id'] for file in current_files}

    # Keep checking for changes
    while True:
        # Sleep for a certain interval before checking again
        time.sleep(60)  # Check every minute

        # Get updated list of files
        updated_files = list_files(folder_id)
        updated_file_ids = {file['id'] for file in updated_files}

        # Find new file ids (those not present in the previous check)
        new_file_ids = updated_file_ids - current_file_ids

        # Print information about new files
        if new_file_ids:
            new_files = [file for file in updated_files if file['id'] in new_file_ids]
            print("New file(s) detected:")
            for file in new_files:
                print(f"Name: {file['name']}, ID: {file['id']}")
            # Update current state with the new files
            current_file_ids = updated_file_ids

# Main Function
if __name__ == '__main__':
    folder_id = 'your_folder_id'  # Replace with your Google Drive folder ID
    check_for_new_files(folder_id)
