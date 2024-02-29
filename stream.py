import streamlit as st
from llama_index.llms import OpenAI
import openai
from llama_index.readers.google import GoogleDriveReader
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, ServiceContext, Document
import os

# Load the .env file
load_dotenv()

# Access the API key from environment variable
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = openai_api_key

# Initialize GoogleDriveReader
loader = GoogleDriveReader()

st.set_page_config(page_title="Chat with the Streamlit docs, powered by LlamaIndex", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Chat with the Streamlit docs, powered by LlamaIndex 💬🦙")
st.info("This is an info message", icon="📃")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Streamlit's open-source Python library!"}
    ]

@st.experimental_singleton(show_spinner=False)
def load_data(folder_id: str):
    with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
        # Load documents from the specified Google Drive folder
        docs = loader.load_data(folder_id=folder_id)
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features."))
        # Create a VectorStoreIndex from the loaded documents
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data(folder_id="1xCRk4ZdPH_OOp2fDulleilxKJEV3_ahD")

if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

prompt = st.text_input("Your question")  # Use text_input instead of chat_input for compatibility

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add response to message history

for message in st.session_state.messages:  # Display the prior chat messages
    st.write(f"{message['role'].capitalize()}: {message['content']}")
