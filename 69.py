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
import re

# Get openai_api_key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

### Copy and paste all the functions as is

def blogPostGenerator(keyword):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to write a blog post based on a user's keyword: '{keyword}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please generate a blog post based on the keyword: '{keyword}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(keyword=keyword)
    return result # returns string   

def include_images(blog_post):
    # Code to include relevant images in the blog post
    # ...
    return blog_post_with_images

def optimize_seo(blog_post_with_images):
    # Remove HTML tags from the blog post
    blog_post_without_tags = re.sub('<.*?>', '', blog_post_with_images)
    
    # Remove special characters from the blog post
    blog_post_without_special_chars = re.sub('[^A-Za-z0-9 ]+', '', blog_post_without_tags)
    
    # Convert the blog post to lowercase
    seo_optimized_blog_post = blog_post_without_special_chars.lower()
    
    return seo_optimized_blog_post

def calculate_seo_score(seo_optimized_blog_post):
    # Calculate the number of words in the blog post
    word_count = len(seo_optimized_blog_post.split())
    
    # Calculate the number of unique words in the blog post
    unique_words = set(seo_optimized_blog_post.split())
    unique_word_count = len(unique_words)
    
    # Calculate the keyword density in the blog post
    keyword_density = seo_optimized_blog_post.count(keyword) / word_count
    
    # Calculate the SEO score
    seo_score = (unique_word_count * keyword_density) / word_count
    
    return seo_score

### Create a form

with st.form(key='seo_blog_post'):
    # Under the form, take all the user inputs
    keyword = st.text_input("Enter keyword")
    submit_button = st.form_submit_button(label='Generate Blog Post')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            blog_post = ""
        elif keyword:
            blog_post = blogPostGenerator(keyword)
        else:
            blog_post = ""
        blog_post_with_images = include_images(blog_post)
        seo_optimized_blog_post = optimize_seo(blog_post_with_images)
        seo_score = calculate_seo_score(seo_optimized_blog_post)
        #Under the st.form_submit_button, show the results.
        if seo_optimized_blog_post:
            st.markdown(seo_optimized_blog_post)
        if seo_score:
            st.info(f"SEO Score: {seo_score}")
#############################################################