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

def load_pdf_content(file_path):
    if file_path != '':
        with open(file_path, 'rb') as file:
            pdf_content = file.read()
        return pdf_content
    else:
        return None

def nameExtractor(pdf_content):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an assistant designed to extract names from the given PDF content."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please extract the names from the following PDF content: '{pdf_content}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(pdf_content=pdf_content)
    return result # returns string   

### Create a form

with st.form(key='pdf_hacker'):
    # Under the form, take all the user inputs
    st.title('PDF Hacker')
    uploaded_file = st.file_uploader("Upload PDF File", type=["pdf"], key='file_path')
    if uploaded_file is not None:
        # Create a temporary file to store the uploaded content
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            file_path = temp_file.name # it shows the file path
    else:
        file_path = ''
    
    submit_button = st.form_submit_button(label='Extract Names')
    
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        pdf_content = load_pdf_content(file_path)
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            extracted_names = ""
        elif pdf_content:
            extracted_names = nameExtractor(pdf_content)
        else:
            extracted_names = ""
        
        #Under the st.form_submit_button, show the results.
        if extracted_names:
            st.write("Extracted Names:")
            for name in extracted_names:
                st.write(name)