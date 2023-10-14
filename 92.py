import time
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders import *
import shutil
import os
import streamlit as st
import tempfile

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.markdown("""# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑
2. Upload a legal document by clicking on the "Legal Document" button.
3. Enter the legal question and risk assessment in the chat input box.
4. Wait for the AI to generate the answer and risk assessment report.
5. View the answer and risk assessment report displayed in the chat.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("🔍Lawyer in a Tap is a comprehensive legal assistant app that helps you navigate complex legal jargon, prepare legal documents, and provides preliminary advice before consulting a lawyer. With features like document interpretation, legal question answering, and risk assessment, Lawyer in a Tap is your go-to resource for all your legal needs.")

st.title('Lawyer in a Tap')
# Get the legal document from the user
uploaded_file = st.file_uploader(
    "Legal Document", type=['pdf', 'docx', 'txt'], key='legal_document')
if uploaded_file is not None:
    # Create a temporary file to store the uploaded content
    extension = uploaded_file.name.split(".")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{extension}') as temp_file:
        temp_file.write(uploaded_file.read())
        legal_document = temp_file.name  # it shows the file path
else:
    legal_document = ''
# Load the legal document as a Document from the file path


def load_document(legal_document):
    if legal_document.endswith('.pdf'):
        loader = UnstructuredPDFLoader(
            legal_document, mode="elements", strategy="fast")
    if legal_document.endswith('.docx'):
        loader = UnstructuredWordDocumentLoader(legal_document)
    if legal_document.endswith('.txt'):
        loader = TextLoader(legal_document)
    docs = loader.load()
    return docs


if legal_document:
    document = load_document(legal_document)
else:
    document = ''
# Convert the Document to a string
document_text = "".join([doc.page_content for doc in document])
# Get the legal question and risk assessment from the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if legal_question_and_risk_assessment := st.chat_input("Enter the legal question and risk assessment"):
    with st.chat_message("user"):
        st.markdown(legal_question_and_risk_assessment)
    st.session_state.messages.append(
        {"role": "user", "content": legal_question_and_risk_assessment})
# Answer the legal question and generate a risk assessment report using the legal document

msgs = StreamlitChatMessageHistory()

prompt = PromptTemplate(
    input_variables=['chat_history', 'document_text', 'legal_question_and_risk_assessment'], template='''You are a legal expert. Answer the legal question and generate a risk assessment report using the provided legal document.

Legal Document:
{document_text}

{chat_history}
Human: {legal_question_and_risk_assessment}
Legal Expert:'''
)
memory = ConversationBufferMemory(
    memory_key="chat_history", input_key="legal_question_and_risk_assessment", chat_memory=msgs, return_messages=True)
if openai_api_key:
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k",
                    openai_api_key=openai_api_key, temperature=0)
    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )
else:
    chat_llm_chain = ''


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    answer_and_risk_assessment_report = ""
elif document_text and legal_question_and_risk_assessment:
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        answer_and_risk_assessment_report = chat_llm_chain.run(
            document_text=document_text, legal_question_and_risk_assessment=legal_question_and_risk_assessment)
else:
    answer_and_risk_assessment_report = ""
# Display the answer and risk assessment report to the user

with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in answer_and_risk_assessment_report.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})
