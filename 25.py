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

st.title('Excel')

def load_doc1(file_path1):
    from langchain.document_loaders.excel import UnstructuredExcelLoader
    loader = UnstructuredExcelLoader(file_path1, mode="elements")
    docs = loader.load()
    return docs

def load_doc2(file_path2):
    from langchain.document_loaders.excel import UnstructuredExcelLoader
    loader = UnstructuredExcelLoader(file_path2, mode="elements")
    docs = loader.load()
    return docs

def compare_excel_files(excel_str1, excel_str2):
    # Compare the two excel files
    if excel_str1 == excel_str2:
        return "The excel files are identical."
    else:
        return "The excel files are different."

with st.form(key='excel_comparison'):
    #Get file path for the first excel file from the user
    uploaded_file1 = st.file_uploader("Upload Excel File", type=["xlsx"], key='file_path1')
    if uploaded_file1 is not None:
        # Create a temporary file to store the uploaded content
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file1.read())
            file_path1 = temp_file.name # it shows the file path
    else:
        file_path1 = ''

    #Get file path for the second excel file from the user
    uploaded_file2 = st.file_uploader("Upload Excel File", type=["xlsx"], key='file_path2')
    if uploaded_file2 is not None:
        # Create a temporary file to store the uploaded content
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file2.read())
            file_path2 = temp_file.name # it shows the file path
    else:
        file_path2 = ''

    if file_path1:
        doc1 = load_doc1(file_path1)
    else:
        doc1 = ''

    if file_path2:
        doc2 = load_doc2(file_path2)
    else:
        doc2 = ''

    excel_str1 = "".join([doc.page_content for doc in doc1])
    excel_str2 = "".join([doc.page_content for doc in doc2])

    submit_button = st.form_submit_button(label='Compare Excel Files')

    if submit_button:
        comparison_result = compare_excel_files(excel_str1, excel_str2)
        if comparison_result:
            st.write(comparison_result)