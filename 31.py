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
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

def scrape_stories():
    # List of countries with royal families
    countries = ['uk', 'sweden', 'norway', 'denmark', 'netherlands', 'spain', 'belgium', 'japan', 'thailand', 'saudi-arabia']
    stories = {}

    for country in countries:
        url = f'https://www.royal.uk/{country}-royal-family'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the top 20 stories
        top_stories = soup.find_all('div', class_='views-row', limit=20)

        # Extract the title and link of each story
        country_stories = []
        for story in top_stories:
            title = story.find('h2').text.strip()
            link = 'https://www.royal.uk' + story.find('a')['href']
            country_stories.append((title, link))

        stories[country] = country_stories

    return stories

def summarize_stories(docs):
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

def storyToBlogConverter(translated_stories):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are a creative assistant tasked with converting translated stories into entertaining blog posts."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Here is the translated story: '{translated_stories}'. Please convert it into an entertaining blog post."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(translated_stories=translated_stories)
    return result # returns string   

def send_email(email_address, blogs):
    # Setup the SMTP server and log into your account
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your-email@gmail.com', 'your-password')

    # Create the email
    email = MIMEMultipart()
    email['From'] = 'your-email@gmail.com'
    email['To'] = email_address
    email['Subject'] = 'RoyalNews Blogs'
    email.attach(MIMEText(blogs, 'plain'))

    # Send the email
    server.send_message(email)
    server.quit()

with st.form(key='story_game'):
    #Get email address from the user
    email_address = st.text_input("Enter your email address")
    submit_button = st.form_submit_button(label='Submit Story')
    # run functions if submit button is pressed
    if submit_button:
        #Scrape the top 20 stories about each country's royal family
        stories = scrape_stories()
        #Convert the scraped stories to Document
        stories_doc =  [Document(page_content=stories, metadata={'source': 'local'})]
        #Summarize the Document of stories
        if stories_doc:
            summarized_stories = summarize_stories(stories_doc)
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
        #Convert the translated stories into entertaining blogs
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            blogs = ""
        elif translated_stories:
            blogs = storyToBlogConverter(translated_stories)
        else:
            blogs = ""
        #Send the blogs to the given email address
        if email_address and blogs:
            send_email(email_address, blogs)
        #Show a confirmation message to the user
        st.success("Operation completed successfully!")