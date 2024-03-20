import streamlit as st
from llama_index.core import VectorStoreIndex, ServiceContext, Document
# Frontend UI
st.title("Intelligent Document Finder")
service_choice = st.radio("Select the service:", ("Google Drive", "OneDrive"))

if service_choice == "Google Drive":
    google_folder_link = st.text_input("Enter your Google Drive folder link:")
    if st.button("Search in Google Drive"):
        # Call the function to handle Google Drive search
        pass  # Replace with actual function call
elif service_choice == "OneDrive":
    onedrive_folder_link = st.text_input("Enter your OneDrive folder link:")
    if st.button("Search in OneDrive"):
        # User Authentication flow: Replace client id with your own id
        # loader = OneDriveReader(client_id="d33f76d2-e4bc-432f-87db-88ffc1e40fc2")
        pass


