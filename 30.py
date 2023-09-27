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

st.title('RoyalNews')

# Function Definitions
def load_sources(source_urls):
    loader = WebBaseLoader(source_urls)
    docs = loader.load()
    return docs

def summarize_sources(docs):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    chain = load_summarize_chain(llm, chain_type="stuff")
    return chain.run(docs)

def storyTranslator(summarized_stories):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are a language translator. Your task is to translate summarized stories into Chinese."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please translate the following summarized story into Chinese: '{summarized_stories}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(summarized_stories=summarized_stories)
    return result # returns string   

def blogFromTranslatedStories(translated_stories,picture_urls):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to generate entertaining blog posts from translated stories and associated picture URLs."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please create a blog post using the translated story: '{translated_stories}' and the picture URL: '{picture_urls}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(translated_stories=translated_stories, picture_urls=picture_urls)
    return result # returns string   

def blogSender(email_address,blogs):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an assistant tasked with sending blogs to a specified email address."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please send the following blogs: {blogs}, to this email address: {email_address}."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(email_address=email_address, blogs=blogs)
    return result # returns string   

with st.form(key='blog_form'):
    #Get email address from the user
    email_address = st.text_input("Enter your email address")
    #Get source URLs from the user
    source_urls = st.text_area("Enter source URLs")
    #Get picture URLs from the user
    picture_urls = st.text_area("Enter picture URLs, separated by commas")
    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        #Load the source URLs as Document
        if source_urls:
            source_docs = load_sources(source_urls)
        else:
            source_docs = ''
        #Summarize the source Documents
        if source_docs:
            summarized_stories = summarize_sources(source_docs)
        else:
            summarized_stories = ""
        #Translate the summarized stories into Chinese
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            translated_stories = ""
        elif summarized_stories:
            translated_stories = storyTranslator(summarized_stories)
        else:
            translated_stories = ""
        #Generate entertaining blogs from the translated stories and picture URLs
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            blogs = ""
        elif translated_stories and picture_urls:
            blogs = blogFromTranslatedStories(translated_stories,picture_urls)
        else:
            blogs = ""
        #Send the blogs to the given email address
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            email_sent = ""
        elif email_address and blogs:
            email_sent = blogSender(email_address,blogs)
        else:
            email_sent = ""
        #Display a confirmation message to the user
        if email_sent:
            st.success("Email has been successfully sent!")