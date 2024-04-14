# Intelligent_Document_Finder

- Streamlit Authentication with Streamlit Authenticator:

Streamlit Authenticator offers a straightforward approach to user authentication within Streamlit applications. In this implementation, a custom database is created within the application to manage user credentials. Users can sign up for an account or log in with existing credentials. This approach provides a hands-on understanding of user interface (UI) design in Streamlit while handling user authentication and authorization.

- FastAPI Authentication with JWT (JSON Web Tokens):
- The main method is by Fast API where endpoints are defined. Upon successful authentication, a JWT token is generated and provided to the client, valid for a specified duration (here for 15 minutes). Subsequent requests to protected endpoints require including this token in the request headers. If the token expires,  i have added models.py and database.py to implement the Postgres database with Fast API
- I have uploaded with dummy database to secure my Postgres credentials.

This project is a Streamlit-based chatbot that leverages the LlamaIndex library to provide a conversational interface for querying and interacting with documents indexed from Google Drive. It uses OpenAI's GPT-3.5-turbo model to generate responses and Streamlit for the web interface.

## Video Link:
https://drive.google.com/drive/folders/14C93jsJmExUUByg6_X07J8BQ2w9-Np68?usp=sharing

## Installation
Prerequisites
Before running this project, some prerequisites need to be installed:

Python 3.6 or higher (i have used python==3.10.0)
A virtual environment (recommended)
Create a virtual environment:

python -m venv venv
Activate the virtual environment:

On Windows:
.\venv\Scripts\activate

1. Clone this repository to your local machine
2. Install the required dependencies using pip:
   pip install -r requirements.txt

     
4. Set up your environment variables by creating a `.env` file in the root directory of the project. Add your OpenAI API key to the `.env` file:
5. Create .streamlit folder and create secrets.toml and add open ai api key [openai_key=”sk-..”]



## Usage

To launch the Streamlit application, run the following command in your terminal:
streamlit run main.py


# Real time data fetching from google drive embedding and indexing is done by using gpt-3.5 turbo model (Here is Some snapshots of while i was testing the project).
## UI of Intelligent Document Finder

![Screenshot (53)](https://github.com/dhruvaditya/Intelligent_Document_Finder/assets/89244720/3f2c6649-18a1-489d-994e-37c9bdc322d3)

## Here is the query response on my local machine during testing:

## Login Page
![Screenshot (612)](https://github.com/dhruvaditya/Intelligent_Document_Finder/assets/89244720/233e74c2-82d7-4ac6-8968-cdd65a8010d1)

## Register Page
![Screenshot (614)](https://github.com/dhruvaditya/Intelligent_Document_Finder/assets/89244720/eac9904a-5102-4dad-84bf-f65047e33545)

## Main Page after Login
![Screenshot (615)](https://github.com/dhruvaditya/Intelligent_Document_Finder/assets/89244720/1cf4d9f5-e196-4a7e-8d30-9420293d6a5f)

# Fast API 
![Screenshot (617)](https://github.com/dhruvaditya/Intelligent_Document_Finder/assets/89244720/efe5ad80-63fc-4ce4-a229-97b01e8666d0)

![Screenshot (54)](https://github.com/dhruvaditya/Intelligent_Document_Finder/assets/89244720/fd9fb0cb-fd37-4d7e-8d50-cada80986f68)

## Flow chart
![Google Drive (3)](https://github.com/dhruvaditya/Intelligent_Document_Finder/assets/89244720/71cb3748-4d91-476f-800b-ffde248433e8)



