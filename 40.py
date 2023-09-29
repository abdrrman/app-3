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
    # Implementation goes here
    
    return svelte_app

def create_sqlite_database():
    # Create a SQLite database to store user logins
    sqlite_database = sqlite3.connect('user_logins.db')
    cursor = sqlite_database.cursor()

    # Create a table to store user logins
    cursor.execute('''CREATE TABLE IF NOT EXISTS logins
                      (username TEXT PRIMARY KEY, password TEXT)''')

    # Commit the changes and close the database connection
    sqlite_database.commit()
    sqlite_database.close()

    return sqlite_database

def create_stripe_integration():
    # Set your secret key: remember to change this to your live secret key in production
    # See your keys here: https://dashboard.stripe.com/apikeys
    stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

    # Create a new Stripe integration for payments
    # Implementation goes here

    return stripe_integration

def foo1():
    result = "res"
    return result

def foo2(half_story,user_choice):
    result = half_story + user_choice
    return result

### Create a form

with st.form(key='story_game'):
    # Under the form, take all the user inputs
    text_input = st.text_input(label='Enter some text')
    user_choice = st.selectbox("What would you like to do next?", ["Choice1", "Choice2"])
    submit_button = st.form_submit_button(label='Submit Story')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        half_story = foo1()
        if half_story:
            #Under the st.form_submit_button, show the results.
            st.write(half_story)
        if text_input and user_choice :
            continued_story = foo2(text_input,user_choice)
        else:
            continued_story = ""
        if continued_story:
            #Under the st.form_submit_button, show the results.
            st.markdown(continued_story)
#############################################################