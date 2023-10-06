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

def load_web_page_content(web_page_address):
    loader = WebBaseLoader([web_page_address])
    docs = loader.load()
    return docs

def summarize_content(docs):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    chain = load_summarize_chain(llm, chain_type="stuff")
    return chain.run(docs)

### Create a form

with st.form(key='web_summary'):
    # Under the form, take all the user inputs
    web_page_address = st.text_input("Enter web page address")
    submit_button = st.form_submit_button(label='Summarize')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        if web_page_address:
            web_content = load_web_page_content(web_page_address)
        else:
            web_content = ''
        # Convert the web page content to a string
        web_string = "".join([doc.page_content for doc in web_content])
        # Summarize the web page content
        if web_content:
            summarized_content = summarize_content(web_content)
        else:
            summarized_content = ""
        # Display the summarized content to the user
        if summarized_content:
            # Under the st.form_submit_button, show the results.
            st.write(summarized_content)