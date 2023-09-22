
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

st.title('Celebrity Parody')
#Get the name of the celebrity from the user
celebrity_name = st.text_input("Enter the name of the celebrity")
#Generate a greeting message as the celebrity
def greetingGenerator(celebrity_name):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are a celebrity. Your task is to generate a greeting message as {celebrity_name}."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Hello, everyone! This is {celebrity_name}. I just wanted to send a quick greeting and let you all know how grateful I am for your support. Thank you for being amazing fans!"""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(celebrity_name=celebrity_name)
    return result # returns string   


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    greeting_message = ""
elif celebrity_name:
    greeting_message = greetingGenerator(celebrity_name)
else:
    greeting_message = ""
#Display the greeting message to the user
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in greeting_message.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
#Get user's message
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])

if user_message := st.chat_input("Type your message"):
    with st.chat_message("user"):
        st.markdown(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})
#Generate a response as the celebrity based on the user's message
def celebrity_response(user_message):
    prompt = PromptTemplate(
        input_variables=['chat_history', 'user_message'], template='''You are a celebrity. Respond to the user's message in a way that reflects your personality and public image.

{chat_history}
User: {user_message}
Celebrity:'''
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
    celebrity_response = ""
elif user_message:
    if 'chat_llm_chain' not in st.session_state:
        st.session_state.chat_llm_chain = celebrity_response(user_message)
    celebrity_response = st.session_state.chat_llm_chain.run(user_message=user_message)
else:
    celebrity_response = ""
#Display the celebrity's response to the user
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in celebrity_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
