# Intelligent_Document_Finder

This project is a Streamlit-based chatbot that leverages the LlamaIndex library to provide a conversational interface for querying and interacting with documents indexed from Google Drive. It uses OpenAI's GPT-3.5-turbo model to generate responses and Streamlit for the web interface.

## Installation
Prerequisites
Before running this project, some prerequisites need to be installed:

Python 3.6 or higher
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


Real time fetching from google drive (Some snapshots of while i was testing the project).
Prompt: There is a pdf file named docu.pdf, Read that pdf and tell me the summary of that pdf only

Response: The PDF file "docu.pdf" contains feedback on a conversation titled "Coffee with Chintan." The author expresses gratitude for the opportunity to participate in the conversation and highlights the insightful knowledge gained from talking with Chintan. The feedback includes details about Chintan's life journey, feedback on gain profiles, the value of time, the company's focus areas, memorable achievements of Promact, advice on work ethic, and insights into Chintan's personal life and routines. The conversation was engaging and informative, lasting for 2 hours, with the promise of future meetings to delve into more topics.
![Screenshot (34)](https://github.com/dhruvaditya/Intelligent_Document_Finder/assets/89244720/3ac779db-f6e4-41c2-b267-281f884a5754)
