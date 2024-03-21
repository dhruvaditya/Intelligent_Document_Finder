import msal
from llama_index.core import VectorStoreIndex, ServiceContext, Document
from msal import PublicClientApplication
from dotenv import load_dotenv
import openai
from llama_index.core import Document, VectorStoreIndex
from llama_index.core.llama_pack import download_llama_pack
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex, ServiceContext, Document
from llama_index.llms.openai import OpenAI
import os


from llama_index.readers.microsoft_onedrive import OneDriveReader
# Load the .env file
load_dotenv()
openai.api_key = os.environ["OPENAI_KEY"]
# User Authentication flow: Replace client id with your own id
client_id = os.getenv('CLIENT_ID')
loader = OneDriveReader(client_id)

# APP Authentication flow: NOT SUPPORTED By Microsoft

#### Get all documents including subfolders.
documents = loader.load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("What to improve in the PPT for SIH")
print(response)