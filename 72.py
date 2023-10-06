# All library imports
import os
import shutil
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
import speech_recognition as sr

# Get openai_api_key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

# Copy and paste all the functions as is
def transcribe_audio(audio_file, input_language):
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Reading Audio file as source
    # listening the audio file and store in audio_text variable
    with sr.AudioFile(audio_file) as source:
        audio_text = r.listen(source)

    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
    try:
        # using google speech recognition
        return r.recognize_google(audio_text, language=input_language)
    except:
        print('Sorry.. run again...')

def audioIdeaGenerator(doc_string):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an AI assistant capable of generating ideas based on the information contained in an audio document."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """The audio document is: '{doc_string}'. Please generate ideas based on the information in this audio."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(doc_string=doc_string)
    return result # returns string   

# Create a form
with st.form(key='audio_idea'):
    # Under the form, take all the user inputs
    uploaded_file = st.file_uploader("Upload Audio File", type=["mp3", "wav"], key='audio_file')
    input_language = st.text_input("Enter the input language")
    submit_button = st.form_submit_button(label='Generate Ideas')

    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        if uploaded_file is not None:
            # Create a temporary file to store the uploaded content
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                audio_file = temp_file.name # it shows the file path
        else:
            audio_file = ''

        # Invoke the function
        transcribed_text = transcribe_audio(audio_file, input_language)
        #Convert the Document object to a string
        doc_string = "".join([doc.page_content for doc in transcribed_text])

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            ideas = ""
        elif doc_string:
            ideas = audioIdeaGenerator(doc_string)
        else:
            ideas = ""

        #Under the st.form_submit_button, show the results.
        if ideas:
            st.success(ideas)