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

def load_documents(document_paths):
    loader = UnstructuredPDFLoader(document_paths)
    docs = loader.load()
    return docs

def LLM_answer_generator(document_strings,question):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are a lawyer that generates answers based on given documents and a question. The given documents are: {document_strings}."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Given the following documents: {document_strings}, and the question: '{question}', please generate the answer in a lawyer style."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(document_strings=document_strings, question=question)
    return result # returns string   

### Create a form

with st.form(key='lovGPT'):
    # Under the form, take all the user inputs
    uploaded_file = st.file_uploader("Upload Document", type=["pdf"], key='document_paths')
    if uploaded_file is not None:
        # Create a temporary file to store the uploaded content
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            document_paths = temp_file.name # it shows the file path
    else:
        document_paths = ''
    
    if document_paths:
        documents = load_documents(document_paths)
    else:
        documents = ''
    
    question = st.text_input("Enter the question")
    
    submit_button = st.form_submit_button(label='Submit')
    
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        document_strings = "".join([doc.page_content for doc in documents])
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            answer = ""
        elif document_strings and question:
            document_strings = "".join([doc.page_content for doc in documents])
            answer = LLM_answer_generator(document_strings,question)
        else:
            answer = ""
        
        #Under the st.form_submit_button, show the results.
        if answer:
            st.write("Answer:", answer)