# import os
# import pandas as pd
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseDownload
# from googleapiclient.http import MediaFileUpload
# import io
# from googleapiclient.errors import HttpError 
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# import google.auth


# #Ok Tested.
# # Define the scopes 
# SCOPES = ['https://www.googleapis.com/auth/drive']

# def authenticate():
#     # Load credentials from credentials.json
#     flow = InstalledAppFlow.from_client_secrets_file(
#         'credentials.json', scopes=SCOPES)
#     creds = flow.run_local_server(port=0)
#     return creds

# def main():
#     # Authenticate and create Google Drive service
#     credentials = authenticate()
#     service = build('drive', 'v3', credentials=credentials)

#     # Now we can use the service to interact with Google Drive API
#     # Specify the folder ID where you want to upload the file
#     folder_id = '1xCRk4ZdPH_OOp2fDulleilxKJEV3_ahD'

#     # Path to the file you want to upload
#     file_path = 'file:///C:/Users/promact.DESKTOP-RHBFB7T/Downloads/streamlit-cheat-sheet.pdf'

#     # Upload the file
#     upload_file(service, file_path, folder_id)


# def upload_file(service, file_path, folder_id):
#     file_name = os.path.basename(file_path)
#     file_metadata = {
#         'name': file_name,
#         'parents': [folder_id]  # Specify the folder ID where you want to upload the file
#     }
#     media = MediaFileUpload(file_path)
#     file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#     print('File ID: %s' % file.get('id')) 


# def upload_basic():
#   """Insert new file.
#   Returns : Id's of the file uploaded

#   Load pre-authorized user credentials from the environment.
#   TODO(developer) - See https://developers.google.com/identity
#   for guides on implementing OAuth2 for the application.
#   """
#   creds, _ = google.auth.default()

#   try:
#     # create drive api client
#     service = build("drive", "v3", credentials=creds)

#     file_metadata = {"name": "download.jpeg"}
#     media = MediaFileUpload("download.jpeg", mimetype="image/jpeg")
#     # pylint: disable=maybe-no-member
#     file = (
#         service.files()
#         .create(body=file_metadata, media_body=media, fields="id")
#         .execute()
#     )
#     print(f'File ID: {file.get("id")}')

#   except HttpError as error:
#     print(f"An error occurred: {error}")
#     file = None

#   return file.get("id")

# if __name__ == "__main__":
#     upload_basic()
########################################################################################
# from google import Create_Service
# CLIENT_SECRET_FILE='credentials.json'
# API_NAME='drive'
# API_VERSION='v3'
# SCOPES=['https://www.googleapis.com/auth/drive']

# service= Create_Service(CLIENT_SECRET_FILE,API_NAME,SCOPES)
# national_parks=['Yellowstone','Rocky Mountain','Yosemite']
# for national_park in national_parks:
#     file_metadata={
#         'name':national_park,
#         'mimeType':'application/vnd.google-apps.folder',
#         'parents':['1xCRk4ZdPH_OOp2fDulleilxKJEV3_ahD']

#     }

#     service.files().create(body=file_metadata).execute()


##############################################################################
# import httplib2  # Assuming you're using httplib2 for authentication

# def Create_Service(client_secret_file, api_name, api_version, scopes):
#     # ... (Implement authentication logic using httplib2 or a suitable library)
#     return service  # Replace with the actual service object

# CLIENT_SECRET_FILE = 'credentials.json'
# API_NAME = 'drive'
# API_VERSION = 'v3'
# SCOPES = ['https://www.googleapis.com/auth/drive']

# service = Create_Service(CLIENT_SECRET_FILE, API_NAME, SCOPES)  # Assuming successful authentication
# national_parks = ['Yellowstone', 'Rocky Mountain', 'Yosemite']

# for national_park in national_parks:
#     file_metadata = {
#         'name': national_park,
#         'mimeType': 'application/vnd.google-apps.folder',
#         'parents': ['1xCRk4ZdPH_OOp2fDulleilxKJEV3_ahD']
#     }

#     service.files().create(body=file_metadata).execute()
#################################################################

#To fetch data from google drive

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


def main():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("drive", "v3", credentials=creds)

    # Call the Drive v3 API
    results = (
        service.files()
        .list(pageSize=10, fields="nextPageToken, files(id, name)")
        .execute()
    )
    items = results.get("files", [])

    if not items:
      print("No files found.")
      return
    print("Files:")
    for item in items:
      print(f"{item['name']} ({item['id']})")
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()