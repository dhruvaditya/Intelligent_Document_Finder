import streamlit as st
import requests

st.title('Simple API Call')

# Define API endpoint
# url = "https://jsonplaceholder.typicode.com/posts"
url= "http://127.0.0.1:8000/testing"

if st.button('Make API Call'):

    # Make GET request
    response = requests.get(url)

    # If the GET request is successful, the status_code will be 200
    if response.status_code == 200:

        # Get the JSON data of the response
        data = response.json()

        # Show the JSON data in Streamlit
        st.write(data)
    else:
        st.write("There was an error with the API call")