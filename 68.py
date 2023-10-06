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

def load_website(url):
    loader = WebBaseLoader([url])
    docs = loader.load()
    return docs

def seoBlogPostGenerator(web_str):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an AI assistant tasked with generating a SEO blog post related to the given content: '{web_str}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please write a blog post with SEO optimization based on the following content: '{web_str}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(web_str=web_str)
    return result # returns string   

### Create a form

with st.form(key='seo_blog_post'):
    # Under the form, take all the user inputs
    url = st.text_input("Enter website URL")
    uploaded_file = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], key='images')
    submit_button = st.form_submit_button(label='Generate Blog Post')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            blog_post = ""
        elif url:
            web_doc = load_website(url)
            web_str = "".join([doc.page_content for doc in web_doc])
            if uploaded_file is not None:
                # Create a temporary file to store the uploaded content
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(uploaded_file.read())
                    images = temp_file.name # it shows the file path
            else:
                images = ''
            if web_str:
                blog_post = seoBlogPostGenerator(web_str)
            else:
                blog_post = ""
        else:
            blog_post = ""
        #Under the st.form_submit_button, show the results.
        if blog_post:
            st.markdown(blog_post)
        #Display the uploaded images to the user
        if images:
            st.image(images, use_column_width=True)