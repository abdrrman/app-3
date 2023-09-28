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

st.title('Hackla')

def load_website(url):
    loader = WebBaseLoader(url)
    docs = loader.load()
    return docs

def blogPostGenerator(web_str):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to write a blog post related to the given string content."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please compose a blog post based on the following string content: '{web_str}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(web_str=web_str)
    return result # returns string   

with st.form(key='blog_post_generator'):
    url = st.text_input("Enter website URL")
    submit_button = st.form_submit_button(label='Generate Blog Post')
    
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
        blog_post = ""
    elif url:
        web_doc = load_website(url)
        web_str = "".join([doc.page_content for doc in web_doc])
        if web_str:
            blog_post = blogPostGenerator(web_str)
        else:
            blog_post = ""
    else:
        blog_post = ""
    
    if blog_post:
        st.markdown(blog_post)