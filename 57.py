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

def blogPostGenerator(title,content,color,font,loading_animation,examples):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to generate a blog post with the provided information."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Title: {title}

Content: {content}

Color: {color}

Font: {font}

Loading Animation: {loading_animation}

Examples: {examples}

Please generate the blog post using this information."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(title=title, content=content, color=color, font=font, loading_animation=loading_animation, examples=examples)
    return result # returns string   

### Create a form

with st.form(key='blog_post_generator'):
    # Under the form, take all the user inputs
    title = st.text_input("Enter the title of the blog post")
    content = st.text_area("Enter the content of the blog post")
    color_scheme = st.selectbox("Select the color scheme", ["Light", "Dark"])
    font = st.text_input("Enter the desired font style")
    loading_animation = st.checkbox("Enable loading animation")
    examples = st.text_area("Enter any examples or references")
    submit_button = st.form_submit_button(label='Generate Blog Post')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            blog_post = ""
        elif title and content and color_scheme and font and loading_animation and examples:
            blog_post = blogPostGenerator(title,content,color_scheme,font,loading_animation,examples)
        else:
            blog_post = ""
        #Under the st.form_submit_button, show the results.
        if blog_post:
            st.markdown(blog_post)