from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Defined the scopes from google drive API v3 documentatin, for the accessibility of the files.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
#Reauthenticated Google drive to resolve the bug that i was facing 
"""An error occurred while downloading file: <HttpError 403 when requesting
 Details: "[{'message': 'The user has not granted the app 471623972493 read access to the file , 'domain': 'global', 'reason': 'appNotAuthorizedToFile', 'location': 'Authorization', 'locationType': 'header'}]">"""
def reauthenticate():
    # Created the flow using the client secrets file from the Google Developer Console
    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)

    # Run the flow to get the new credentials
    creds = flow.run_local_server(port=0)

    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    return creds

# Call the reauthenticate function to get new credentials
creds = reauthenticate()

