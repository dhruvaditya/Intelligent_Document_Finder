import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from llama_index.readers.google import GoogleDriveReader
import openai
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex

# Load environment variables from .env file
load_dotenv()
# Retrieve the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

loader = GoogleDriveReader()
def load_data(folder_id: str):
    docs = loader.load_data(folder_id=folder_id)
    for doc in docs:
        doc.id_ = doc.metadata["file_name"]
    return docs


docs = load_data(folder_id="1xCRk4ZdPH_OOp2fDulleilxKJEV3_ahD")

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


#To query the text
#To query the text and print the result
def query(index):
    query_engine = index.as_query_engine()
    response = query_engine.query("summarize the file")
    print(response)

# Call the Drive v3 API
def list_files(service, folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    docs = loader.load_data(folder_id=folder_id)
    for doc in docs:
             doc.id_ = doc.metadata["file_name"]
    # index = VectorStoreIndex.from_documents(items)
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:

            print(u'{0} ({1})'.format(item['name'], item['id']))
    # return index

#adding the folder id here
service = service_account_login()
store=list_files(service, '1RFhr3-KmOZCR5rtp4dlOMNl3LKe1kOA5')
# query(store)



# loader = GoogleDriveReader()
# def load_data(service, folder_id: str):
#     results = service.files().list(
#         q=f"'{folder_id}' in parents",
#         pageSize=10, fields="nextPageToken, files(id, name)").execute()
#     items = results.get('files', [])
#     if not items:
#         print('No files found.')
#     else:
#          docs = loader.load_data(folder_id=folder_id)
#     for doc in docs:
#         doc.id_ = doc.metadata["file_name"]
#     return docs


# docs = load_data(service,folder_id="1RFhr3-KmOZCR5rtp4dlOMNl3LKe1kOA5")
# print(docs)
# def load_data(service, folder_id: str):
#     # Assuming service is a properly initialized Google Drive API service
#     results = service.files().list(
#         q=f"'{folder_id}' in parents",
#         pageSize=10, fields="nextPageToken, files(id, name)").execute()
#     items = results.get('files', [])
#     if not items:
#         print('No files found.')
#         return []  # Return an empty list if no files are found
#     else:
#         loader = GoogleDriveReader()
#         docs = loader.load_data(folder_id=folder_id)
#         for doc in docs:
#             doc.id_ = doc.metadata["file_name"]
#         return docs


#   # This is just a placeholder
# folder_id = "1RFhr3-KmOZCR5rtp4dlOMNl3LKe1kOA5"  # folder id where data is stored

# docs = load_data(service, folder_id)
# print(docs)