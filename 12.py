
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

openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

st.title('Elon')
#Generate a prompt to create a conversation with Elon Musk
def elonMuskPromptGenerator():
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are tasked with generating a prompt to create a conversation with Elon Musk."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Create a prompt that can initiate an interesting conversation with Elon Musk."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run({})
    return result # returns string   

conversation_prompt = elonMuskPromptGenerator()
#Start a chat-based conversation with the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])

while True:
    user_message = st.chat_input("User:")
    if user_message:
        with st.chat_message("user"):
            st.markdown(user_message)
        st.session_state.messages.append({"role": "user", "content": user_message})
        break
#Generate a response from the Elon Musk clone based on the user's message
def elon_musk_clone(conversation_prompt,user_message):
    prompt = PromptTemplate(
        input_variables=['chat_history', 'conversation_prompt', 'user_message'], template='''You are an AI model that emulates Elon Musk. Generate a response based on the user's message.

Conversation Prompt: {conversation_prompt}

{chat_history}
User: {user_message}
Elon Musk Clone:'''
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="user_message")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", openai_api_key=openai_api_key, temperature=0.7)
    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )
    return chat_llm_chain
    

if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    elon_response = ""
elif conversation_prompt and user_message:
    if 'chat_llm_chain' not in st.session_state:
        st.session_state.chat_llm_chain = elon_musk_clone(conversation_prompt,user_message)
    elon_response = st.session_state.chat_llm_chain.run(conversation_prompt=conversation_prompt, user_message=user_message)
else:
    elon_response = ""
#Display the response from the Elon Musk clone to the user
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in elon_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
