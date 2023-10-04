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

# Get openai_api_key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

### Copy and paste all the functions as is

def blogPostGenerator(title,content,keywords):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to write a blog post based on the given title, content, and keywords."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Title: {title}

Content: {content}

Keywords: {keywords}

Please compose a blog post using the provided information."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(title=title, content=content, keywords=keywords)
    return result # returns string   

### Create a form

with st.form(key='blog_post_generator'):
    # Under the form, take all the user inputs
    title = st.text_input("Enter the title of the blog post")
    content = st.text_area("Enter the content of the blog post")
    keywords = st.text_input("Enter keywords for the blog post")
    submit_button = st.form_submit_button(label='Generate Blog Post')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            blog_post = ""
        elif title and content and keywords:
            blog_post = blogPostGenerator(title,content,keywords)
        else:
            blog_post = ""
        #Under the st.form_submit_button, show the results.
        if blog_post:
            st.markdown(blog_post)
#############################################################