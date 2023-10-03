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

def webSearch(search_query):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an AI assistant tasked with searching the web for the latest AI tools using the search query: '{search_query}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please search the web for the latest AI tools using the search query: '{search_query}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(search_query=search_query)
    return result # returns string   

### Create a form

with st.form(key='web_search'):
    # Under the form, take all the user inputs
    search_query = st.text_input("Enter the search query")
    submit_button = st.form_submit_button(label='Search')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            search_results = ""
        elif search_query:
            search_results = webSearch(search_query)
        else:
            search_results = ""
        #Under the st.form_submit_button, show the results.
        if search_results:
            st.markdown(search_results)
