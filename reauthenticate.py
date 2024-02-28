from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Define the scopes your application requires
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def reauthenticate():
    # Create the flow using the client secrets file from the Google Developer Console
    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)

    # Run the flow to get the new credentials
    creds = flow.run_local_server(port=0)

    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    return creds

# Call the reauthenticate function to get new credentials
creds = reauthenticate()

# Now you can use these credentials to create a service object
# and make calls to the Google Drive API
