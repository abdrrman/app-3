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

st.title('youttube insights')

def load_video_content(youtube_video_url):
    from langchain.document_loaders import WebBaseLoader
    
    if youtube_video_url:
        loader = WebBaseLoader(youtube_video_url)
        video_doc = loader.load()
    else:
        video_doc = ''
    
    return video_doc

def videoInsights(video_str):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an AI assistant tasked with generating insights from a video {video_str}."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please watch the video {video_str} and provide three exciting insights."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(video_str=video_str)
    return result # returns string   

with st.form(key='youtube_insights'):
    youtube_video_url = st.text_input("Enter YouTube video URL")
    submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        video_doc = load_video_content(youtube_video_url)
        video_str = "".join([doc.page_content for doc in video_doc])
        insights = videoInsights(video_str)
        if insights:
            st.info(insights)