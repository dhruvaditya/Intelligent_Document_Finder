import streamlit as st
from llama_index.readers.google import GoogleDriveReader
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Access the API key
openai_api_key = os.environ.get("OPENAI_API_KEY")
# os.environ["OPENAI_API_KEY"] = ""
loader = GoogleDriveReader()
def load_data(folder_id: str):
    docs = loader.load_data(folder_id=folder_id)
    for doc in docs:
        doc.id_ = doc.metadata["file_name"]
    return docs


docs = load_data(folder_id="1xCRk4ZdPH_OOp2fDulleilxKJEV3_ahD")
# print(docs)
nodes = pipeline.run(documents=docs)
print(f"Ingested {len(nodes)} Nodes")
query_engine = index.as_query_engine()
response = query_engine.query("What are the sub-types of question answering?")
print(str(response))