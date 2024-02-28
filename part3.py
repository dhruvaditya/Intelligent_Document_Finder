#Ok Tested Loader working Google drive Reader


import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from llama_index.readers.google import GoogleDriveReader
import openai
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from dotenv import load_dotenv
# from llama_index.core import llama-index-embeddings-openai
# Load the .env file
load_dotenv()

# Access the API key
openai_api_key = os.environ.get("OPENAI_API_KEY")

# documents = SimpleDirectoryReader("data").load_data()


gauth=GoogleAuth()
drive=GoogleDrive(gauth)

loader = GoogleDriveReader()
def load_data(folder_id: str):
    docs = loader.load_data(folder_id=folder_id)
    
    # for doc in docs:
    #     doc.id_ = doc.metadata["file_name"]
    return docs


docs = load_data(folder_id="1xCRk4ZdPH_OOp2fDulleilxKJEV3_ahD")
print(docs)