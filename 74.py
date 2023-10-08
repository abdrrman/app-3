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

st.title('Hangman')

# Copy and paste all the functions as is
def start_game(word_to_guess, player_name):
    # Initialize the game state
    game_state = {
        'word_to_guess': word_to_guess,
        'player_name': player_name,
        'guessed_letters': [],
        'remaining_attempts': len(word_to_guess) + 2,  # Allow 2 extra attempts
    }
    return game_state

def update_game_state(game_state, guessed_letter):
    # Add the guessed letter to the list of guessed letters
    game_state['guessed_letters'].append(guessed_letter)
    # If the guessed letter is not in the word to guess, decrease the remaining attempts
    if guessed_letter not in game_state['word_to_guess']:
        game_state['remaining_attempts'] -= 1
    return game_state

# Create a form
with st.form(key='hangman_game'):
    # Under the form, take all the user inputs
    word_to_guess = st.text_input("Enter the word to guess")
    player_name = st.text_input("Enter player's name")
    guessed_letter = st.text_input("Enter your guessed letter")
    submit_button = st.form_submit_button(label='Start Game')

    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Start the game with the word to guess and player's name
        game_state = start_game(word_to_guess, player_name)
        # Update the game state with the guessed letter
        updated_game_state = update_game_state(game_state, guessed_letter)
        # Show the current game state to the user
        if updated_game_state:
            st.write(updated_game_state)
        # At the end of the game, show the final score to the user
        if updated_game_state:
            st.success(f"Final Score: {updated_game_state['score']}")