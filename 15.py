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

def load_document(document_path):
    loader = TextLoader(document_path) 
    docs = loader.load()
    return docs

def emailIdeaGenerator(product_description,target_audience,main_argument,document_str):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to generate email ideas for a product. The product is described as '{product_description}', the target audience is '{target_audience}', and the main argument is '{main_argument}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Based on the product description, target audience, and main argument, please generate 10 email ideas. Also, consider the document string: '{document_str}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(product_description=product_description, target_audience=target_audience, main_argument=main_argument, document_str=document_str)
    return result # returns string   

st.title('Email Ideas')

with st.form(key='email_ideas_form'):
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        placeholder="sk-...",
        value=os.getenv("OPENAI_API_KEY", ""),
        type="password",
    )
    product_description = st.text_area("Enter product description")
    target_audience = st.text_input("Enter target audience")
    main_argument = st.text_input("Enter the main argument")
    uploaded_file = st.file_uploader("Upload Document", type=["txt", "docx", "pdf"])
    submit_button = st.form_submit_button(label='Generate Email Ideas')

    if submit_button:
        if uploaded_file is not None:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                st.session_state['document_path'] = temp_file.name
        else:
            st.session_state['document_path'] = ''

        if st.session_state['document_path']:
            document = load_document(st.session_state['document_path'])
        else:
            document = ''

        document_str = "".join([doc.page_content for doc in document])

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            email_ideas = ""
        elif product_description and target_audience and main_argument and document_str:
            email_ideas = emailIdeaGenerator(product_description,target_audience,main_argument,document_str)
        else:
            email_ideas = ""

        if email_ideas:
            st.success(email_ideas)