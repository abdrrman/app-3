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

st.title('CarLeads')

# Copy and paste all the functions as is
def invoiceGenerator(make,model,zip_code):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an assistant designed to generate an invoice for a vehicle. The vehicle's make is '{make}', model is '{model}', and the zip code is '{zip_code}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please generate an invoice for the {make} {model} located in zip code {zip_code}."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(make=make, model=model, zip_code=zip_code)
    return result # returns string   

# Create a form
with st.form(key='invoice_form'):
    # Under the form, take all the user inputs
    make = st.text_input("Enter the make of the vehicle")
    model = st.text_input("Enter the model of the vehicle")
    zip_code = st.text_input("Enter your zip code")
    submit_button = st.form_submit_button(label='Generate Invoice')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            invoice = ""
        elif make and model and zip_code:
            invoice = invoiceGenerator(make,model,zip_code)
        else:
            invoice = ""
        # Under the st.form_submit_button, show the results.
        if invoice:
            st.table(invoice)