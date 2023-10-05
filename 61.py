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
import json
from react_jsonschema_form import SchemaForm

# Get openai_api_key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title('RJSF Boss')

# Copy and paste all the functions as is
def generate_react_form(json_schema, form_data):
    # Convert the json schema and form data from string to dictionary
    json_schema = json.loads(json_schema)
    form_data = json.loads(form_data)
    
    # Generate the react form
    react_form = SchemaForm(schema=json_schema, formData=form_data)
    
    return react_form

# Create a form
with st.form(key='react_form'):
    # Under the form, take all the user inputs
    json_schema = st.text_area("Enter JSON schema")
    form_data = st.text_input("Enter form data")
    submit_button = st.form_submit_button(label='Generate Form')
    
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Invoke the function with the provided arguments
        react_form = generate_react_form(json_schema, form_data)
        
        # Under the st.form_submit_button, show the results.
        if react_form:
            st.code(react_form, language='jsx')