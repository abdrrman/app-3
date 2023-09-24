
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
#Get speech samples of Bill Gates from the user
uploaded_file = st.file_uploader("Upload Bill Gates Speech Samples", type=["txt"])
if uploaded_file is not None:
    # Create a temporary file to store the uploaded content
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        st.session_state['bill_gates_speech_samples'] = temp_file.name # it shows the file path
else:
    st.session_state['bill_gates_speech_samples'] = ''
#Load the speech samples as Document from the file path
###
def load_speech_samples(bill_gates_speech_samples):
    from langchain.document_loaders import TextLoader
    loader = TextLoader(bill_gates_speech_samples) 
    docs = loader.load()
    return docs

if bill_gates_speech_samples:
    speech_doc = load_speech_samples(bill_gates_speech_samples)
else:
    speech_doc = ''
###

Please replace "bill_gates_speech_samples" with the actual path of your text file.
#Convert Document to string content
speech_str = "".join([doc.page_content for doc in speech_doc])
#Get user's input for conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])

if user_input_for_conversation := st.chat_input("Enter your message"):
    with st.chat_message("user"):
        st.markdown(user_input_for_conversation)
    st.session_state.messages.append({"role": "user", "content": user_input_for_conversation})
#Generate the response coming from the virtual clone of Bill Gates
def virtual_clone_of_bill_gates(speech_str,user_input_for_conversation):
    prompt = PromptTemplate(
        input_variables=['chat_history', 'speech_str', 'user_input_for_conversation'], template='''You are a virtual clone of Bill Gates. Respond to the user's input in a way that Bill Gates would.

{chat_history}
User: {user_input_for_conversation}
Bill Gates:'''
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="user_input_for_conversation")
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
    clone_response = ""
elif speech_str and user_input_for_conversation:
    if 'chat_llm_chain' not in st.session_state:
        st.session_state.chat_llm_chain = virtual_clone_of_bill_gates(speech_str,user_input_for_conversation)
    clone_response = st.session_state.chat_llm_chain.run(speech_str=speech_str, user_input_for_conversation=user_input_for_conversation)
else:
    clone_response = ""
#Display the response from the virtual clone of Bill Gates to the user
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in clone_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
