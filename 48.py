# All library imports
import os
import shutil
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

# Get openai_api_key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

# Copy and paste all the functions as is

# Function to authenticate user
def authenticate_user(google_login_credentials):
    try:
        # Load the credentials from the provided string
        credentials = service_account.Credentials.from_service_account_info(google_login_credentials)
        # If the credentials are valid, return True
        return True
    except DefaultCredentialsError:
        # If the credentials are not valid, return False
        return False

def feedbackSummarizer(road_selection,rating,feedback):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an assistant designed to summarize user's rating and feedback for a specific road selection."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """The user selected the road: {road_selection}. They rated it {rating} and their feedback was: '{feedback}'. Please summarize this information."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(road_selection=road_selection, rating=rating, feedback=feedback)
    return result # returns string   

# Create a form
with st.form(key='road_rater'):
    # Under the form, take all the user inputs
    google_login_credentials = st.text_input("Enter your Google login credentials")
    road_selection = st.selectbox("Select the road", ["Road 1", "Road 2", "Road 3", "Road 4", "Road 5"])
    rating = st.slider("Rate the selected road", 1, 5)
    feedback = st.text_area("Enter your feedback for the selected road")
    submit_button = st.form_submit_button(label='Submit Feedback')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        authentication_status = authenticate_user(google_login_credentials)
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            summary = ""
        elif road_selection and rating and feedback:
            summary = feedbackSummarizer(road_selection,rating,feedback)
        else:
            summary = ""
        # Under the st.form_submit_button, show the results.
        if summary:
            st.warning(summary)