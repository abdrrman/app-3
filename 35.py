import os
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

with st.form(key='zombie_game'):
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        placeholder="sk-...",
        value=os.getenv("OPENAI_API_KEY", ""),
        type="password",
    )

    st.title('The Walking LLM')
    #Get the location of the zombies from the user
    zombie_location = st.text_input("Enter the location of the zombies")
    #Get the weapon choice from the user
    weapon_choice = st.radio("Choose a weapon", ["Sword", "Bow", "Axe", "Staff"])
    #Get the survival strategy from the user
    survival_strategy = st.radio("Select the survival strategy", ["Fight", "Flight", "Freeze"])
    submit_button = st.form_submit_button(label='Submit Story')

    #Generate a response for navigating the zombie apocalypse
    def zombieApocalypseNavigator(zombie_location,weapon_choice,survival_strategy):
        chat = ChatOpenAI(
            model="gpt-3.5-turbo-16k",
            openai_api_key=openai_api_key,
            temperature=0.7
        )
        system_template = """You are a survival expert providing guidance during the zombie apocalypse."""
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_template = """You are currently located in {zombie_location}. Your weapon of choice is {weapon_choice}. Your survival strategy is {survival_strategy}. Please provide guidance on how to navigate the zombie apocalypse."""
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        chain = LLMChain(llm=chat, prompt=chat_prompt)
        result = chain.run(zombie_location=zombie_location, weapon_choice=weapon_choice, survival_strategy=survival_strategy)
        return result # returns string   

    if submit_button:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            response = ""
        elif zombie_location and weapon_choice and survival_strategy:
            response = zombieApocalypseNavigator(zombie_location,weapon_choice,survival_strategy)
        else:
            response = ""
        #Display the response to the user
        if response:
            st.write(response)
    else: # if not submitted yet, we need to initizalize response to get rid of name error
        response = ""