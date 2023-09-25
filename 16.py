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

st.title('Email ideas')

def load_document(document_path):
    if document_path.endswith('.txt'):
        loader = TextLoader(document_path)
    elif document_path.startswith('http'):
        if document_path.endswith('.pdf'):
            loader = OnlinePDFLoader(document_path)
        else:
            loader = WebBaseLoader(document_path)
    elif document_path.endswith('.pdf'):
        loader = UnstructuredPDFLoader(document_path, mode="elements", strategy="fast")
    elif document_path.endswith('.ppt') or document_path.endswith('.pptx'):
        loader = UnstructuredPowerPointLoader(document_path, mode="elements", strategy="fast")
    elif document_path.endswith('.csv'):
        loader = UnstructuredCSVLoader(document_path, mode="elements")
    elif document_path.endswith('.xls') or document_path.endswith('.xlsx'):
        loader = UnstructuredExcelLoader(document_path, mode="elements")
    else:
        raise ValueError('Unsupported file type')
    
    docs = loader.load()
    return docs

def emailIdeaGenerator(document_str,product_description,target_audience,main_argument):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to generate email ideas based on the provided document, product description, target audience, and main argument."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Based on the document: '{document_str}', the product description: '{product_description}', the target audience: '{target_audience}', and the main argument: '{main_argument}', please generate some email ideas."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(document_str=document_str, product_description=product_description, target_audience=target_audience, main_argument=main_argument)
    return result # returns string   

with st.form(key='email_ideas_form'):
    openai_api_key = st.text_input(
        "OpenAI API Key",
        placeholder="sk-...",
        value=os.getenv("OPENAI_API_KEY", ""),
        type="password",
    )
    uploaded_file = st.file_uploader("Upload Your Document", type=["txt", "docx", "pdf"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            st.session_state['document_path'] = temp_file.name
    else:
        st.session_state['document_path'] = ''
    document_path = st.session_state['document_path']
    if document_path:
        document = load_document(document_path)
    else:
        document = ''
    product_description = st.text_area("Enter product description")
    target_audience = st.text_input("Enter the target audience")
    main_argument = st.text_input("Enter the main argument")
    document_str = "".join([doc.page_content for doc in document])
    submit_button = st.form_submit_button(label='Generate Email Ideas')
    if submit_button:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            email_ideas = ""
        elif document_str and product_description and target_audience and main_argument:
            email_ideas = emailIdeaGenerator(document_str,product_description,target_audience,main_argument)
        else:
            email_ideas = ""
        if email_ideas:
            st.success(email_ideas)