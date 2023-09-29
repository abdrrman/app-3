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
import sqlite3
import stripe

# Get openai_api_key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

### Copy and paste all the functions as is

def create_svelte_app():
    # Create a new Svelte SSR app for the sound sample product catalog
    svelte_app = "Svelte SSR app created"
    return svelte_app

def create_sqlite_database():
    # Connect to the SQLite database
    conn = sqlite3.connect('user_logins.db')
    c = conn.cursor()

    # Create the user logins table
    c.execute('''CREATE TABLE IF NOT EXISTS user_logins
                 (username TEXT, password TEXT)''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def create_stripe_integration():
    # Set the Stripe API key
    stripe.api_key = os.getenv("STRIPE_API_KEY")

    # Create a new Stripe integration
    stripe_integration = stripe.Integration.create(
        name="My Stripe Integration",
        type="payment",
        enabled=True
    )

    return stripe_integration

### Create a form

with st.form(key='story_game'):
    # Under the form, take all the user inputs
    svelte_app = create_svelte_app()
    create_sqlite_database()
    stripe_integration = create_stripe_integration()
    submit_button = st.form_submit_button(label='Submit Story')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        #Under the st.form_submit_button, show the results.
        st.title('waveboundsounds')
        st.write(svelte_app)
        st.write(sqlite_database)
        st.write(stripe_integration)
#############################################################