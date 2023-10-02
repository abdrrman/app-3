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

st.title('AI LAwyer')

# Copy and paste all the functions as is
def legalAdvisor(legal_query):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are a virtual legal advisor. Your task is to provide legal advice based on the given query."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """The legal query is: '{legal_query}'. Please provide appropriate legal advice."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(legal_query=legal_query)
    return result # returns string   

# Create a form
with st.form(key='legal_query_form'):
    # Under the form, take all the user inputs
    legal_query = st.text_input("Enter your legal query")
    submit_button = st.form_submit_button(label='Submit Query')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            legal_advice = ""
        elif legal_query:
            legal_advice = legalAdvisor(legal_query)
        else:
            legal_advice = ""
        # Under the st.form_submit_button, show the results.
        if legal_advice:
            st.warning(legal_advice)