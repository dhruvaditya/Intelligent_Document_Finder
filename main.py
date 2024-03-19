import uvicorn
from fastapi import FastAPI, Body, Depends
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
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from dotenv import load_dotenv
from llama_index.core import Document, VectorStoreIndex
from llama_index.core.llama_pack import download_llama_pack
from fastapi import Depends
from app.auth.model import UserSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

# Load the .env file
load_dotenv()
openai.api_key = os.environ["OPENAI_KEY"]

gauth=GoogleAuth()
drive=GoogleDrive(gauth)

# Initialize GoogleDriveReader
loader = GoogleDriveReader()

users = []

app = FastAPI()


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False
# testing
@app.get("/", tags=["test"])
def greet():
    return {"hello": "world!."}
@app.post("/folders", dependencies=[Depends(JWTBearer())], tags=["drivereader"])
async def get_index(folder_id: str):
  #loading data from google drive reader
  docs = loader.load_data(folder_id=folder_id)
  service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an advanced AI assistant with the capability to securely access and retrieve information from a specified Google Drive account. Your primary function is to provide accurate and detailed answers to queries based on the content stored within documents in the Google Drive. You have read-only access to an extensive collection of documents, spreadsheets, presentations, and other files that you can reference to extract information. Structure your response to each query as follows: Response: [Your direct answer], Source: [File Name].[File Type], Location: Page [number] or Section [name], and Author Name."))
  index = VectorStoreIndex.from_documents(docs)

  if folder_id:
      return index
  else:
      return {"message": "Please provide a folder ID in the query string"}

@app.post("/askquestion", dependencies=[Depends(get_index)], tags=["drivereader"])
async def ask_question(prompt: str,index: VectorStoreIndex = Depends(get_index)):
    #it will take questions from the user and process it using llamaindex and return response
    query_engine = index.as_query_engine()
    response = query_engine.query(prompt)
    return response


@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(...)):
    users.append(user) # can replace with postgres by using db.add(), i have used this method only for testing.
    return signJWT(user.email)

#Post method to user login
@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    #to check user credentials using JWT Token
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
