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
from jsonschema import validate

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Get openai_api_key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

st.title('RJSF Boss')

# Copy and paste all the functions as is
def generate_react_form(json_schema, form_data):
    # Validate the form data against the JSON schema
    try:
        validate(instance=form_data, schema=json_schema)
        return True
    except Exception as e:
        return str(e)

# Create a form
with st.form(key='my_form'):
    # Under the form, take all the user inputs
    json_schema = st.text_area("Enter JSON schema")
    form_data = st.text_input(label='Enter some data')
    submit_button = st.form_submit_button(label='Submit')

    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Invoke the function with provided arguments
        react_form = generate_react_form(json_schema, form_data)
        # Under the st.form_submit_button, show the results.
        if react_form:
            st.code(react_form, language='jsx')