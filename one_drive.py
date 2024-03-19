import msal
from msal import PublicClientApplication
# APPLICATION_ID='5bb08096-5db5-44ad-9fc2-48cc773ca582'
# CLIENT_SECRET='YKV8Q~zkNg-9nuW91~cJeY.lpun_bRo0eSni3bTl'

from llama_index.readers.microsoft_onedrive import OneDriveReader
APPLICATION_ID='d33f76d2-e4bc-432f-87db-88ffc1e40fc2'
# User Authentication flow: Replace client id with your own id
loader = OneDriveReader(client_id="d33f76d2-e4bc-432f-87db-88ffc1e40fc2")

# APP Authentication flow: NOT SUPPORTED By Microsoft

#### Get all documents including subfolders.
documents = loader.load_data()

print(documents)