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

st.title('excel')
#Get file path for the first excel file from the user
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file is not None:
    # Create a temporary file to store the uploaded content
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        file_path1 = temp_file.name # it shows the file path
        st.session_state['file_path1'] = file_path1
else:
    file_path1 = ''
#Load the first excel file as Document from the file path
def load_doc1(file_path1):
    from langchain.document_loaders.excel import UnstructuredExcelLoader
    loader = UnstructuredExcelLoader(file_path1, mode="elements")
    docs = loader.load()
    return docs

if file_path1:
    doc1 = load_doc1(file_path1)
else:
    doc1 = ''
#Convert the first excel file Document to string
excel_str1 = "".join([doc.page_content for doc in doc1])
#Get file path for the second excel file from the user
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file is not None:
    # Create a temporary file to store the uploaded content
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        file_path2 = temp_file.name # it shows the file path
        st.session_state['file_path2'] = file_path2
else:
    file_path2 = ''
#Load the second excel file as Document from the file path
def load_doc2(file_path2):
    from langchain.document_loaders.excel import UnstructuredExcelLoader
    loader = UnstructuredExcelLoader(file_path2, mode="elements")
    docs = loader.load()
    return docs

if file_path2:
    doc2 = load_doc2(file_path2)
else:
    doc2 = ''
#Convert the second excel file Document to string
excel_str2 = "".join([doc.page_content for doc in doc2])
#Compare the two excel files
def excelComparator(excel_str1,excel_str2):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an assistant tasked with comparing two Excel files."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please compare the following Excel files: {excel_str1} and {excel_str2}."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(excel_str1=excel_str1, excel_str2=excel_str2)
    return result # returns string   

with st.form(key='excel_comparison'):
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
        comparison_result = ""
    elif excel_str1 and excel_str2:
        comparison_result = excelComparator(excel_str1,excel_str2)
    else:
        comparison_result = ""
    if comparison_result:
        st.write(comparison_result)
    submit_button = st.form_submit_button(label='Submit Comparison')