
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

st.title('HRAI')
#Get resume from the user
uploaded_file = st.file_uploader("Upload Your Resume", type=["txt"])
if uploaded_file is not None:
    # Create a temporary file to store the uploaded content
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        st.session_state['resume_path'] = temp_file.name # it shows the file path
else:
    st.session_state['resume_path'] = ''
#Load the resume as Document from the file path
from langchain.document_loaders import TextLoader

def load_resume(resume_path):
    loader = TextLoader(resume_path) 
    docs = loader.load()
    return docs

if resume_path:
    resume_doc = load_resume(resume_path)
else:
    resume_doc = ''
#Convert the Document object of the resume to string
resume_string = "".join([doc.page_content for doc in resume_doc])
#Analyze the resume
def resumeAnalyzer(resume_string):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an assistant designed to analyze a resume. Your task is to provide a detailed analysis of the given resume."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please analyze the following resume: '{resume_string}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(resume_string=resume_string)
    return result # returns string   


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    analyzed_resume = ""
elif resume_string:
    analyzed_resume = resumeAnalyzer(resume_string)
else:
    analyzed_resume = ""
#Show the result of the resume analysis to the user
if analyzed_resume:
    st.write(analyzed_resume)
#Get job posting from the user
job_posting = st.text_area("Enter job posting")
#Optimize the job posting
def jobPostingOptimizer(job_posting):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to optimize job postings to attract more qualified candidates."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """The job posting is: '{job_posting}'. Please optimize it."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(job_posting=job_posting)
    return result # returns string   


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    optimized_job_posting = ""
elif job_posting:
    optimized_job_posting = jobPostingOptimizer(job_posting)
else:
    optimized_job_posting = ""
#Show the optimized job posting to the user
if optimized_job_posting:
    st.success(optimized_job_posting)
#Get candidate queries from the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])

if candidate_queries := st.chat_input("Enter the candidate queries"):
    with st.chat_message("user"):
        st.markdown(candidate_queries)
    st.session_state.messages.append({"role": "user", "content": candidate_queries})
#Respond to candidate queries
def respond_to_candidate_queries(candidate_queries):
    prompt = PromptTemplate(
        input_variables=['chat_history', 'candidate_queries'], template='''You are a chatbot designed to respond to candidate queries about a job application process. 

{chat_history}
Candidate: {candidate_queries}
Chatbot:'''
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="candidate_queries")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", openai_api_key=openai_api_key, temperature=0)
    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )
    return chat_llm_chain
    

if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    response_to_queries = ""
elif candidate_queries:
    if 'chat_llm_chain' not in st.session_state:
        st.session_state.chat_llm_chain = respond_to_candidate_queries(candidate_queries)
    response_to_queries = st.session_state.chat_llm_chain.run(candidate_queries=candidate_queries)
else:
    response_to_queries = ""
#Show the response to the user
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in response_to_queries.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
#Get employee surveys from the user
employee_surveys = st.text_area("Enter employee surveys")
#Analyze the surveys
def surveyAnalyzer(employee_surveys):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an assistant designed to analyze employee surveys."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please analyze the following employee surveys: '{employee_surveys}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(employee_surveys=employee_surveys)
    return result # returns string   


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    analyzed_surveys = ""
elif employee_surveys:
    analyzed_surveys = surveyAnalyzer(employee_surveys)
else:
    analyzed_surveys = ""
#Show the result of the survey analysis to the user
if analyzed_surveys:
    st.table(analyzed_surveys)
#Get employee feedback from the user
employee_feedback = st.text_area("Enter your feedback")
#Analyze the feedback
def feedbackAnalyzer(employee_feedback):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an assistant designed to analyze employee feedback."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please analyze the following feedback: '{employee_feedback}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(employee_feedback=employee_feedback)
    return result # returns string   


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    analyzed_feedback = ""
elif employee_feedback:
    analyzed_feedback = feedbackAnalyzer(employee_feedback)
else:
    analyzed_feedback = ""
#Show the result of the feedback analysis to the user
if analyzed_feedback:
    st.write(analyzed_feedback)
#Get event details from the user
event_details = st.text_area("Enter event details")
#Plan the event
def eventPlanner(event_details):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an event planner. Your task is to plan an event based on the given details."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """The event details are: {event_details}. Please plan the event accordingly."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(event_details=event_details)
    return result # returns string   


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    planned_event = ""
elif event_details:
    planned_event = eventPlanner(event_details)
else:
    planned_event = ""
#Show the planned event to the user
if planned_event:
    st.success(planned_event)
