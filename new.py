import streamlit as st
import jwt
import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from llama_index.core import VectorStoreIndex, ServiceContext, Document
from llama_index.llms.openai import OpenAI
import openai
import os
from hashlib import sha256
from dotenv import load_dotenv
from llama_index.core import Document, VectorStoreIndex
from llama_index.core.llama_pack import download_llama_pack
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from llama_index.readers.google import GoogleDriveReader
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import msal
from msal import PublicClientApplication
from llama_index.readers.microsoft_onedrive import OneDriveReader
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
load_dotenv()
openai.api_key = os.environ["OPENAI_KEY"]
# Secret key for JWT encoding and decoding
SECRET_KEY = "c75273f47181c55aa70c010d2deb885a"

#gauth is a class provided by PyDrive that handles authentication and creates a GoogleAuth object.
#it initiates the OAuth 2.0 authentication flow, which is the process that google uses to provide authorization and authentication
#it is fetching client_secrets.json file which is a json file downloaded from google drive console inorder to make connection with the application
gauth=GoogleAuth()
drive=GoogleDrive(gauth)

# Initialize GoogleDriveReader
loader = GoogleDriveReader()
#for one drive authentication
client_id = os.getenv('CLIENT_ID')
loader_one = OneDriveReader(client_id)
def generate_token(username):
    # Token expires in 30 minutes
    expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
    token = jwt.encode({'username': username, 'exp': expiration_time}, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        st.error('Token has expired, please log in again.')
        return None
    except jwt.InvalidTokenError:
        st.error('Invalid token, please log in again.')
        return None

def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Dummy user database
users_db = {
    "adi": {
        "username": "adi",
        "password_hash": hash_password("123"),  # Password is storing in the database after hashed
    }
}

def login(username, password):
    user = users_db.get(username)
    if user and user['password_hash'] == hash_password(password):
        token = generate_token(username)
        st.session_state['token'] = token
        st.session_state['username'] = username
        st.success('Logged in successfully!','This is the next page')
    else:
        st.error('Invalid username or password')

def logout():
    if 'token' in st.session_state:
        del st.session_state['token']
        del st.session_state['username']
    st.info('Logged out.')

# UI for login
if 'token' not in st.session_state:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            login(username, password)

# UI for logout
if 'token' in st.session_state:
    if st.button('Logout'):
        logout()

# Protected content
if 'token' in st.session_state:
    username = verify_token(st.session_state['token'])
    if username:
        st.write(f"Welcome {username}! to Intelligent Document Finder.")
        st.title("Intelligent Document Finder, powered by LlamaIndex 🏆💬🦙")
        st.info("Made with ❤ by Aditya Raj", icon="👩‍💻")
        service_choice = st.radio("Select the service:", ("Google Drive", "OneDrive"))
        if service_choice == "Google Drive":
            google_folder_link = st.text_input("Enter your Google Drive folder link:")
            if st.button("Search in Google Drive"):
                openai.api_key = st.secrets.openai_key
                if "messages" not in st.session_state.keys(): 
                    st.session_state.messages = [
                        {"role": "assistant", "content": "Ask me a question realted to your various types of documents stored in Google Drive"}
                    ]
                @st.cache_resource(show_spinner=False)
                def load_data(folder_id: str):
                    with st.spinner(text="Loading and indexing the Google drive docs – hang tight! This should take 1-2 minutes."):
                        docs = loader.load_data(folder_id=folder_id)
                        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an advanced AI assistant with the capability to securely access and retrieve information from a specified Google Drive account. Your primary function is to provide accurate and detailed answers to queries based on the content stored within documents in the Google Drive. You have read-only access to an extensive collection of documents, spreadsheets, presentations, and other files that you can reference to extract information. Structure your response to each query as follows: Response: [Your direct answer], Source: [File Name].[File Type], Location: Page [number] or Section [name], and Author Name."))
                        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
                        return index
                index = load_data(folder_id=google_folder_link)
                if "chat_engine" not in st.session_state.keys():
                    st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
                if prompt := st.chat_input("Your question"): 
                    st.session_state.messages.append({"role": "user", "content": prompt})
                for message in st.session_state.messages: 
                    with st.chat_message(message["role"]):
                        st.write(message["content"])
                if st.session_state.messages[-1]["role"] != "assistant":
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking takes some time wait..."):
                            response = st.session_state.chat_engine.chat(prompt)
                            st.write(response.response)
                            message = {"role": "assistant", "content": response.response}
                            st.session_state.messages.append(message) 
            
        elif service_choice == "OneDrive":
            onedrive_folder_link = st.text_input("Enter your OneDrive folder link:")
            if st.button("Search in OneDrive"):
                openai.api_key = st.secrets.openai_key
                if "messages" not in st.session_state.keys(): 
                    st.session_state.messages = [
                        {"role": "assistant", "content": "Ask me a question realted to your various types of documents stored in One Drive"}
                    ]
                @st.cache_resource(show_spinner=False)
                def load_data(folder_id: str):
                    with st.spinner(text="Loading and indexing the One drive docs – hang tight! This should take 1-2 minutes."):
                        docs = loader_one.load_data(folder_id=folder_id)
                        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an advanced AI assistant with the capability to securely access and retrieve information from a specified Google Drive account. Your primary function is to provide accurate and detailed answers to queries based on the content stored within documents in the Google Drive. You have read-only access to an extensive collection of documents, spreadsheets, presentations, and other files that you can reference to extract information. Structure your response to each query as follows: Response: [Your direct answer], Source: [File Name].[File Type], Location: Page [number] or Section [name], and Author Name."))
                        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
                        return index
                index = load_data(folder_id=onedrive_folder_link)
                if "chat_engine" not in st.session_state.keys():
                    st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
                if prompt := st.chat_input("Your question"): 
                    st.session_state.messages.append({"role": "user", "content": prompt})
                for message in st.session_state.messages: 
                    with st.chat_message(message["role"]):
                        st.write(message["content"])
                if st.session_state.messages[-1]["role"] != "assistant":
                     with st.chat_message("assistant"):
                         with st.spinner("Thinking takes some time wait..."):
                             response = st.session_state.chat_engine.chat(prompt)
                             st.write(response.response)
                             message = {"role": "assistant", "content": response.response}
                             st.session_state.messages.append(message)

                






elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

try:
    email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(preauthorization=False)
    if email_of_registered_user:
        st.success('User registered successfully')
except Exception as e:
    st.error(e)


with open('./config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)