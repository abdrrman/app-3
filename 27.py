
import os
import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.document_loaders import *
from langchain.chains.summarize import load_summarize_chain
import tempfile
from langchain.docstore.document import Document
import time
from langchain.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

st.title('MarketinGPT')
#Get the Google Drive folder path from the user
Google_Drive_folder = st.text_input("Enter your Google Drive folder path")
#Load the contents of the Google Drive folder
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def load_folder_contents(folder_id):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)", q="'{}' in parents".format(folder_id)).execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

if Google_Drive_folder:
    knowledge_base_doc = load_folder_contents(Google_Drive_folder)
else:
    knowledge_base_doc = ''
#Convert the Document to string content
knowledge_base_str = "".join([doc.page_content for doc in knowledge_base_doc])
#Index the contents into a vector database
# Importing required libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def index_contents(knowledge_base_str):
    # Initialize the TfidfVectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the data
    vector_database = vectorizer.fit_transform([knowledge_base_str])

    return vector_database

# Invoke the function using the provided arguments
vector_database = index_contents(knowledge_base_str)
#Get the OpenAI API key from the user
OpenAI_API_key = st.text_input("Enter your OpenAI API key")
#Get the message from the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])

if message := st.chat_input("Type your message"):
    with st.chat_message("user"):
        st.markdown(message)
    st.session_state.messages.append({"role": "user", "content": message})
#Search the vector database for relevant information related to the message
# Importing required libraries
from sklearn.feature_extraction.text import CountVectorizer

def search_database(message, vector_database):
    # Initialize the CountVectorizer
    count_vectorizer = CountVectorizer()

    # Fit and transform the data
    message_vector = count_vectorizer.fit_transform([message])

    # Calculate the cosine similarity
    similarity_scores = cosine_similarity(message_vector, vector_database)

    # Get the index of the most similar document
    most_similar_index = np.argmax(similarity_scores)

    # Return the most similar document
    return vector_database[most_similar_index]

# Invoke the function using the provided arguments
relevant_info = search_database(message, vector_database)
#Send the relevant information along with the message to the LLM
def send_info_to_LLM(message,relevant_info,OpenAI_API_key):
    prompt = PromptTemplate(
        input_variables=['chat_history', 'message', 'relevant_info', 'OpenAI_API_key'], template='''You are a chatbot having a conversation with a human. You are supposed to send the relevant information along with the message to the LLM. 

Relevant Information: {relevant_info}

{chat_history}
Human: {message}
Chatbot:'''
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="message")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", openai_api_key=openai_api_key, temperature=0)
    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )
    return chat_llm_chain
    

if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    response = ""
elif message and relevant_info and OpenAI_API_key:
    if 'chat_llm_chain' not in st.session_state:
        st.session_state.chat_llm_chain = send_info_to_LLM(message,relevant_info,OpenAI_API_key)
    response = st.session_state.chat_llm_chain.run(message=message, relevant_info=relevant_info, OpenAI_API_key=OpenAI_API_key)
else:
    response = ""
#Display the response to the user with chat interface
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
