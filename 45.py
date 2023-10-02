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
from langchain.prompts import PromptTemplate
import requests

# Get openai_api_key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

### Copy and paste all the functions as is

def searchQueryGenerator(question,country):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an assistant designed to help users generate search queries based on questions and countries."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Combine the question '{question}' with the country '{country}' to form a search query."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(question=question, country=country)
    return result # returns string   

def search_web(search_query):
    url = f"https://www.google.com/search?q={search_query}"
    response = requests.get(url)
    return response.text

def searchResponseGenerator(search_results):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an AI assistant that generates responses based on search results."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Based on the search results: {search_results}, please provide a relevant response."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(search_results=search_results)
    return result # returns string   

def questionSuggester(response):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an assistant designed to provide suggestions for follow-up questions based on the user's response."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Based on the user's response: '{response}', please provide some suggestions for follow-up questions."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(response=response)
    return result # returns string   

### Create a form

with st.form(key='story_game'):
    # Under the form, take all the user inputs
    question = st.text_input("Enter the question")
    country = st.text_input("Enter the country name")
    submit_button = st.form_submit_button(label='Submit Story')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            search_query = ""
        elif question and country:
            search_query = searchQueryGenerator(question,country)
        else:
            search_query = ""
        search_results = search_web(search_query)
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            response = ""
        elif search_results:
            response = searchResponseGenerator(search_results)
        else:
            response = ""
        if response:
            st.write(response)
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            suggestions = ""
        elif response:
            suggestions = questionSuggester(response)
        else:
            suggestions = ""
        if suggestions:
            st.write("Suggestions:")
            for suggestion in suggestions:
                st.write("- " + suggestion)