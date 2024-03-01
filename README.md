# Intelligent_Document_Finder

This project is a Streamlit-based chatbot that leverages the LlamaIndex library to provide a conversational interface for querying and interacting with documents indexed from Google Drive. It uses OpenAI's GPT-3.5-turbo model to generate responses and Streamlit for the web interface.

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

## Usage

To launch the Streamlit application, run the following command in your terminal:
streamlit run main.py


# Real time data fetching from google drive embedding and indexing is done by using gpt-3.5 turbo model (Here is Some snapshots of while i was testing the project).
## UI of Intelligent Document Finder

![Screenshot (53)](https://github.com/dhruvaditya/Intelligent_Document_Finder/assets/89244720/3f2c6649-18a1-489d-994e-37c9bdc322d3)

## Here is the query response on my local machine during testing:

![Screenshot (54)](https://github.com/dhruvaditya/Intelligent_Document_Finder/assets/89244720/fd9fb0cb-fd37-4d7e-8d50-cada80986f68)


