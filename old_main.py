#OK tested with Streamlit UI
import streamlit as st
from llama_index.core import VectorStoreIndex, ServiceContext, Document
from llama_index.llms.openai import OpenAI
import openai
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from llama_index.readers.google import GoogleDriveReader
from dotenv import load_dotenv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from dotenv import load_dotenv
from llama_index.core import Document, VectorStoreIndex
from llama_index.core.llama_pack import download_llama_pack

# download and install dependencies
FuzzyCitationEnginePack = download_llama_pack(
    "FuzzyCitationEnginePack", "./fuzzy_citation_pack"
)

# Load the .env file
load_dotenv()
openai.api_key = os.environ["OPENAI_KEY"]

#gauth is a class provided by PyDrive that handles authentication and creates a GoogleAuth object.
#it initiates the OAuth 2.0 authentication flow, which is the process that google uses to provide authorization and authentication
#it is fetching client_secrets.json file which is a json file downloaded from google drive console inorder to make connection with the application
gauth=GoogleAuth()
drive=GoogleDrive(gauth)

# Initialize GoogleDriveReader
loader = GoogleDriveReader()

st.set_page_config(page_title="Intelligent Document Finder", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
#created a .streamlit folder in the root directory and inside that folder created secrets.toml file. In that file openai_key ="sk-..." is stored
#streamlit is fetching api key from that folder.
openai.api_key = st.secrets.openai_key
st.title("✔ Intelligent Document Finder, powered by LlamaIndex 🏆💬🦙")
st.info("Made with ❤ by Aditya Raj", icon="👩‍💻")
#Initializing the chat history here
if "messages" not in st.session_state.keys(): 
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question realted to your various types of documents stored in Google Drive"}
    ]

@st.cache_resource(show_spinner=False)
def load_data(folder_id: str):
    with st.spinner(text="Loading and indexing the Google drive docs docs – hang tight! This should take 1-2 minutes."):
        # Load documents from the specified Google Drive folder
        docs = loader.load_data(folder_id=folder_id)
        #Service context method called model gpt - 3.5 turbo is used along with system_prompt.
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an advanced AI assistant with the capability to securely access and retrieve information from a specified Google Drive account. Your primary function is to provide accurate and detailed answers to queries based on the content stored within documents in the Google Drive. You have read-only access to an extensive collection of documents, spreadsheets, presentations, and other files that you can reference to extract information. Structure your response to each query as follows: Response: [Your direct answer], Source: [File Name].[File Type], Location: Page [number] or Section [name], and Author Name."))
        #Automatically indexing and Embedding is done here and stored in VectorStoreIndex after loading all the data from google drive folder ID
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index
    
#Function call with folder id passed to index all the unstructured data located to that folder ID
index = load_data(folder_id="Replace with your folder ID")

# Initializing the chat engine

if "chat_engine" not in st.session_state.keys(): 
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

# Prompt to take user input and save it in history
if prompt := st.chat_input("Your question"): 
    st.session_state.messages.append({"role": "user", "content": prompt})

# Displaying the prior chat messages
for message in st.session_state.messages: 
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking takes some time wait..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            #Append the response to the conversation log.
            st.session_state.messages.append(message) 
