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

st.title('gmm app')
#Get cluster data from the user
with st.form(key='cluster_data'):
    cluster_data = st.file_uploader("Upload cluster data file")
    submit_button = st.form_submit_button(label='Submit Cluster Data')

#Analyze the separability of the two clusters using GMM in Python
def gmmAnalyzer(cluster_data):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are a data analyst tasked with analyzing the separability of two clusters using Gaussian Mixture Models (GMM) in Python. The cluster data is given as {cluster_data}."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please analyze the separability of the given cluster data using GMM in Python. The cluster data is given as {cluster_data}."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(cluster_data=cluster_data)
    return result # returns string   

if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    separability = ""
elif submit_button and cluster_data:
    separability = gmmAnalyzer(cluster_data)
else:
    separability = ""
#Display the separability of the two clusters to the user
if separability:
    st.write("The separability of the two clusters is:", separability)