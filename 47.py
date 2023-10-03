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

# Get openai_api_key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

### Copy and paste all the functions as is

def calculate_result(measurement_type, value):
    if measurement_type == "Length":
        result = value * 2.54
    elif measurement_type == "Weight":
        result = value * 0.453592
    elif measurement_type == "Volume":
        result = value * 0.0295735
    else:
        result = None
    return result

### Create a form

with st.form(key='calculator'):
    # Under the form, take all the user inputs
    measurement_type = st.selectbox("Select the measurement type", ["Length", "Weight", "Volume"])
    value = st.number_input("Enter the value of the measurement")
    submit_button = st.form_submit_button(label='Calculate')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        result = calculate_result(measurement_type, value)
        #Under the st.form_submit_button, show the results.
        if result:
            st.write(result)
#############################################################