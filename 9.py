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

def load_codebase(file_path):
    if file_path.endswith('.txt'):
        loader = TextLoader(file_path)
    elif file_path.startswith('http'):
        if file_path.endswith('.pdf'):
            loader = OnlinePDFLoader(file_path)
        else:
            loader = WebBaseLoader(file_path)
    elif file_path.endswith('.pdf'):
        loader = UnstructuredPDFLoader(file_path, mode="elements", strategy="fast")
    elif file_path.endswith('.ppt') or file_path.endswith('.pptx'):
        loader = UnstructuredPowerPointLoader(file_path, mode="elements", strategy="fast")
    elif file_path.endswith('.csv'):
        loader = UnstructuredCSVLoader(file_path, mode="elements")
    elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
        loader = UnstructuredExcelLoader(file_path, mode="elements")
    else:
        raise ValueError('Unsupported file type')
    
    docs = loader.load()
    return docs

def streamlitChatbotGenerator(codebase_str):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are a software assistant capable of generating a Streamlit chatbot UI/UX with st.status, callback handlers, etc."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please generate a Streamlit chatbot UI/UX based on the provided codebase: '{codebase_str}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(codebase_str=codebase_str)
    return result # returns string   

st.title('Streamlit Reforger')

with st.form(key='chatbot_form'):
    openai_api_key = st.text_input(
        "OpenAI API Key",
        placeholder="sk-...",
        value=os.getenv("OPENAI_API_KEY", ""),
        type="password",
    )
    uploaded_file = st.file_uploader("Upload Codebase File", type=["txt"])
    submit_button = st.form_submit_button(label='Generate Chatbot')
    if submit_button:
        if uploaded_file is not None:
            # Create a temporary file to store the uploaded content
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                st.session_state['file_path'] = temp_file.name # it shows the file path
        else:
            st.session_state['file_path'] = ''
        if st.session_state['file_path']:
            codebase_doc = load_codebase(st.session_state['file_path'])
        else:
            codebase_doc = ''
        codebase_str = "".join([doc.page_content for doc in codebase_doc])
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            chatbot_ui = ""
        elif codebase_str:
            chatbot_ui = streamlitChatbotGenerator(codebase_str)
        else:
            chatbot_ui = ""
        st.markdown(chatbot_ui)