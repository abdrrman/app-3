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

def greetingGenerator():
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to generate greeting messages."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please generate a greeting message."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run({})
    return result # returns string   

### Create a form

with st.form(key='greeting_form'):
    # Under the form, take all the user inputs
    submit_button = st.form_submit_button(label='Generate Greeting')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        greeting_message = greetingGenerator()
        #Under the st.form_submit_button, show the results.
        if greeting_message:
            st.write(greeting_message)
#############################################################