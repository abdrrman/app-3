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

st.title('Mavel Hangman')

# Define the function check_guess
def check_guess(guess, scoreboard):
    # Check if the guess is in the word
    if guess in word:
        # If the guess is correct, update the scoreboard
        scoreboard = [guess if letter == guess else score for letter, score in zip(word, scoreboard)]
    else:
        # If the guess is incorrect, decrement the score
        scoreboard = [score - 1 for score in scoreboard]
    return scoreboard

# Create a form
with st.form(key='hangman_game'):
    # Under the form, take all the user inputs
    guess = st.text_input("Enter your guess")
    submit_button = st.form_submit_button(label='Submit Guess')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Invoke the function with the provided arguments
        updated_scoreboard = check_guess(guess, scoreboard)
        # Under the st.form_submit_button, show the results.
        if updated_scoreboard:
            st.table(updated_scoreboard)