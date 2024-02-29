#OK Tested main file
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
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

# Load the .env file
load_dotenv()

# Access the API key
openai_api_key = os.environ.get("OPENAI_API_KEY")
gauth=GoogleAuth()
drive=GoogleDrive(gauth)

# Initialize GoogleDriveReader
loader = GoogleDriveReader()
chroma_client = chromadb.PersistentClient()
chroma_collection = chroma_client.create_collection("quickstart")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

def load_data(folder_id: str):
    # Load documents from the specified Google Drive folder
    docs = loader.load_data(folder_id=folder_id)
    
    # Create a VectorStoreIndex from the loaded documents
    # index = VectorStoreIndex.from_documents(docs)
    index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)
    
    # Create a query engine from the index
    query_engine = index.as_query_engine()
    
    # Perform a query against the index
    response = query_engine.query("There is a pdf file named docu.pdf, Read that pdf and tell me the life lessons from that pdf only")
    print(response)
    
    # Assign a new id_ attribute to each document based on its file name
    
    return docs

# Load documents from the specified folder ID and print them
docs = load_data(folder_id="1xCRk4ZdPH_OOp2fDulleilxKJEV3_ahD")
# print(docs)
