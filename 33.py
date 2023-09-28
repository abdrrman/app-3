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

with st.form(key='hackla_form'):
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        placeholder="sk-...",
        value=os.getenv("OPENAI_API_KEY", ""),
        type="password",
    )

    st.title('Hackla')
    #Get the URL of the website from the user
    url = st.text_input("Enter website URL")
    #Get the name of the platform from the user
    platform_name = st.text_input("Enter the name of the platform")
    #Get the target audience of the platform from the user
    target_audience = st.text_input("Enter the target audience")
    #Get the desired features of the website from the user
    features = st.multiselect("Select the desired features", ["Responsive Design", "User-friendly Interface", "Search Functionality", "Social Media Integration", "E-commerce Functionality"])
    #Get the desired design style of the website from the user
    design_style = st.text_input("Enter the desired design style")
    #Generate a description for the website using the provided inputs
    def websiteDescriptionGenerator(platform_name,target_audience,features,design_style):
        chat = ChatOpenAI(
            model="gpt-3.5-turbo-16k",
            openai_api_key=openai_api_key,
            temperature=0.7
        )
        system_template = """You are an AI assistant tasked with generating a description for a website."""
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_template = """Create a description for a website called {platform_name}. This website is designed for {target_audience} and offers features such as {features}. The design style should be {design_style}."""
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        chain = LLMChain(llm=chat, prompt=chat_prompt)
        result = chain.run(platform_name=platform_name, target_audience=target_audience, features=features, design_style=design_style)
        return result # returns string   

    submit_button = st.form_submit_button(label='Generate Description')

    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
        description = ""
    elif submit_button and platform_name and target_audience and features and design_style:
        description = websiteDescriptionGenerator(platform_name,target_audience,features,design_style)
    else:
        description = ""
    #Display the generated description to the user
    if description:
        st.info(description)