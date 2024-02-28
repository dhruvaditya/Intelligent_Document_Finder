#Ok Tested


import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.readers.google import GoogleDriveReader
import io
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient import errors
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
# SCOPES=['https://www.googleapis.com/auth/drive.readonly']

def service_account_login():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)
def print_file_content(service, file_id):
    try:
        # Request to get the file's metadata and content
        request = service.files().get_media(fileId=file_id)
        # Use io.BytesIO buffer to store the downloaded content
        fh = io.BytesIO()
        # Create a downloader object to download the file
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        # The file's content is now in fh, which acts like a file object.
        # We can read its content and decode if necessary (for text files).
        fh.seek(0)
        content = fh.read().decode('utf-8')
        print(content)
    except errors.HttpError as error:
        print(f'An error occurred: {error}')
    except UnicodeDecodeError as error:
        print(f'Cannot decode file content: {error}')

# Existing function to list files
def list_files(service, folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

def create_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        print(f"Directory '{directory_name}' created.")
    else:
        print(f"Directory '{directory_name}' already exists.")

def download_file(service, file_id, directory_name='docu'):
    try:
        # Get the file's metadata to determine the file's name
        file_metadata = service.files().get(fileId=file_id, fields='name').execute()
        file_name = file_metadata.get('name')

        # If the file has a name, proceed with the download
        if file_name:
            # Ensure the directory exists
            create_directory(directory_name)

            # Define the full path where the file will be saved
            file_path = os.path.join(directory_name, file_name)

            # Request to get the file's content
            request = service.files().get_media(fileId=file_id)
            # Use io.BytesIO buffer to store the downloaded content
            fh = io.BytesIO()
            # Create a downloader object to download the file
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.")
            # The file's content is now in fh, which acts like a file object.
            # Now we can write its content to the local file path.
            with open(file_path, 'wb') as f:
                fh.seek(0)
                f.write(fh.read())
            print(f"File '{file_path}' downloaded successfully.")
        else:
            print("File name not found.")
    except errors.HttpError as error:
        print(f'An error occurred: {error}')


service = service_account_login()
# Assuming 'service' is an authenticated Google Drive service instance
# and 'folder_id' is the ID of the folder you want to list files from
list_files(service, '1xCRk4ZdPH_OOp2fDulleilxKJEV3_ahD')

# To print the content of a file, call the print_file_content function
# with the service object and the file ID you want to print the content of
# print_file_content(service, '1tTd_OpFf01ycEmoiwtBH1moS32ASGqky')
download_file(service, '1tTd_OpFf01ycEmoiwtBH1moS32ASGqky')


# load_data('1xCRk4ZdPH_OOp2fDulleilxKJEV3_ahD')