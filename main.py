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
import openai
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
openai.api_key = os.environ["OPENAI_KEY"]
gauth=GoogleAuth()
drive=GoogleDrive(gauth)

# Initialize GoogleDriveReader
loader = GoogleDriveReader()

st.set_page_config(page_title="Intelligent Document Finder", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
openai.api_key = st.secrets.openai_key
st.title("Intelligent Document Finder, powered by LlamaIndex 💬🦙")
st.info("Made with ❤ by Aditya Raj", icon="👩‍💻")
#Initializing the chat history here
if "messages" not in st.session_state.keys(): 
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question realted to your documents stored in Google Drive"}
    ]

@st.cache_resource(show_spinner=False)
def load_data(folder_id: str):
    with st.spinner(text="Loading and indexing the Google Drive docs – hang tight! This should take 1-2 minutes."):
        # Load documents from the specified Google Drive folder
        docs = loader.load_data(folder_id=folder_id)
        #Service context method called
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features."))
        #indexing and Embedding is done and stored in VectorStoreIndex after loading all the data from google drive folder ID
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index
    
#Function call with folder id passed to index all the unstructured data located to that folder ID
index = load_data(folder_id="1BSY94ha-XX1m27vLUZBmurgrKoV7jRvp")

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
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history