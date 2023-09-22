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

#Generate the adventure game
def gameDesigner(event,choice_1,choice_2,choice_3):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are a game designer tasked with creating an adventure game. You need to design a scenario based on the given event and provide three choices for the player."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """The event is: '{event}'. The choices are: 1) {choice_1}, 2) {choice_2}, and 3) {choice_3}. Please design the game scenario."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(event=event, choice_1=choice_1, choice_2=choice_2, choice_3=choice_3)
    return result # returns string   

st.title('Adventure')

with st.form(key='game_design'):
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        placeholder="sk-...",
        value=os.getenv("OPENAI_API_KEY", ""),
        type="password",
    )
    #Get event from the user
    event = st.text_input("Enter event")
    #Get first choice from the user
    choice_1 = st.text_input("Enter your first choice")
    #Get second choice from the user
    choice_2 = st.text_input("Enter your second choice")
    #Get third choice from the user
    choice_3 = st.text_input("Enter your third choice")
    submit_button = st.form_submit_button(label='Generate Game')

    if submit_button:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            game = ""
        elif event and choice_1 and choice_2 and choice_3:
            game = gameDesigner(event,choice_1,choice_2,choice_3)
        else:
            game = ""
        #Display the generated game to the user
        if game:
            st.write(game)