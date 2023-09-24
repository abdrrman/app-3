
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

st.title('Smartbank')
#Get path of the CSV file that the user upload
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
if uploaded_file is not None:
    # Create a temporary file to store the uploaded content
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        csv_file_path = temp_file.name # it shows the file path
        st.session_state['csv_file_path'] = csv_file_path
else:
    csv_file_path = ''
    st.session_state['csv_file_path'] = csv_file_path
#Load the CSV document from the given path
from langchain.document_loaders.csv_loader import UnstructuredCSVLoader

def load_csv(csv_file_path):
    loader = UnstructuredCSVLoader(csv_file_path, mode="elements") 
    docs = loader.load()
    return docs

if csv_file_path:
    csv_doc = load_csv(csv_file_path)
else:
    csv_doc = ''
#Convert the CSV document to string
csv_str = "".join([doc.page_content for doc in csv_doc])
#Get call destination from the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])

if call_destination := st.chat_input("Enter the call destination"):
    with st.chat_message("user"):
        st.markdown(call_destination)
    st.session_state.messages.append({"role": "user", "content": call_destination})
#Generate the response coming from the agent
def generate_agent_response(csv_str,call_destination):
    prompt = PromptTemplate(
        input_variables=['chat_history', 'csv_str', 'call_destination'], template='''You are a chatbot having a conversation with a human. You are supposed to generate a response based on the given CSV string and call destination.

CSV String: {csv_str}
Call Destination: {call_destination}

{chat_history}
Human: 
Chatbot:'''
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="call_destination")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", openai_api_key=openai_api_key, temperature=0.7)
    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )
    return chat_llm_chain
    

if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    agent_response = ""
elif csv_str and call_destination:
    if 'chat_llm_chain' not in st.session_state:
        st.session_state.chat_llm_chain = generate_agent_response(csv_str,call_destination)
    agent_response = st.session_state.chat_llm_chain.run(csv_str=csv_str, call_destination=call_destination)
else:
    agent_response = ""
#Display the agent's response to the user
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in agent_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
