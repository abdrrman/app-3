
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

st.title('LLM Legal Assistan')
#Get case law or legal judgment from the user
case_law_or_legal_judgment = st.text_area("Enter case law or legal judgment")
#Summarize the given case law or legal judgment
def legalSummarizer(case_law_or_legal_judgment):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are a legal assistant tasked with summarizing the given case law or legal judgment: '{case_law_or_legal_judgment}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please provide a concise summary of the following case law or legal judgment: '{case_law_or_legal_judgment}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(case_law_or_legal_judgment=case_law_or_legal_judgment)
    return result # returns string   


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    summarized_case_law = ""
elif case_law_or_legal_judgment:
    summarized_case_law = legalSummarizer(case_law_or_legal_judgment)
else:
    summarized_case_law = ""
#Display the summarized case law or legal judgment to the user
if summarized_case_law:
    st.success(summarized_case_law)
#Get legal document type from the user
legal_document_type = st.selectbox("Select the type of legal document", ["Contract", "Agreement", "Will", "Power of Attorney", "Deed", "Affidavit"])
#Get user context from the user
user_context = st.text_area("Enter user context")
#Generate a draft for the legal document based on the user's input
def legalDocumentGenerator(legal_document_type,user_context):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are a legal assistant, tasked with drafting a {legal_document_type} based on the user's context."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """The user needs a {legal_document_type}. The context provided by the user is: '{user_context}'. Please draft the document accordingly."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(legal_document_type=legal_document_type, user_context=user_context)
    return result # returns string   


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    legal_draft = ""
elif legal_document_type and user_context:
    legal_draft = legalDocumentGenerator(legal_document_type,user_context)
else:
    legal_draft = ""
#Display the legal draft to the user
if legal_draft:
    st.text(legal_draft)
#Get legal query from the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])

if legal_query := st.chat_input("Enter your legal query"):
    with st.chat_message("user"):
        st.markdown(legal_query)
    st.session_state.messages.append({"role": "user", "content": legal_query})
#Generate a response for the legal query
def legal_advisor_response(legal_query):
    prompt = PromptTemplate(
        input_variables=['chat_history', 'legal_query'], template='''You are a legal advisor. Respond to the legal query as accurately as possible.

{chat_history}
Client: {legal_query}
Legal Advisor:'''
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="legal_query")
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
    legal_response = ""
elif legal_query:
    if 'chat_llm_chain' not in st.session_state:
        st.session_state.chat_llm_chain = legal_advisor_response(legal_query)
    legal_response = st.session_state.chat_llm_chain.run(legal_query=legal_query)
else:
    legal_response = ""
#Display the legal response to the user
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in legal_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
#Get historical legal decisions from the user
historical_legal_decisions = st.text_area("Enter historical legal decisions")
#Analyze the evolution of legal principles over time
def legalAnalyst(historical_legal_decisions):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are a legal analyst. Your task is to analyze the evolution of legal principles over time based on the given historical legal decisions."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please analyze the following historical legal decisions: '{historical_legal_decisions}' and explain how legal principles have evolved over time."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(historical_legal_decisions=historical_legal_decisions)
    return result # returns string   


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    historical_analysis = ""
elif historical_legal_decisions:
    historical_analysis = legalAnalyst(historical_legal_decisions)
else:
    historical_analysis = ""
#Display the historical analysis to the user
if historical_analysis:
    st.write(historical_analysis)
#Get user's practice area
user_practice_area = st.text_input("Enter your practice area")
#Generate a news feed tailored to the user's specific area of practice
def newsFeedGenerator(user_practice_area):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are a news feed generator, tasked with creating a news feed tailored to the user's specific area of practice: '{user_practice_area}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please generate a news feed related to the area of practice: {user_practice_area}."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(user_practice_area=user_practice_area)
    return result # returns string   


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    legal_news_digest = ""
elif user_practice_area:
    legal_news_digest = newsFeedGenerator(user_practice_area)
else:
    legal_news_digest = ""
#Display the legal news digest to the user
if legal_news_digest:
    st.write(legal_news_digest)
#Get AI client interaction from the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])

if AI_client_interaction := st.chat_input("Describe the AI client interaction"):
    with st.chat_message("user"):
        st.markdown(AI_client_interaction)
    st.session_state.messages.append({"role": "user", "content": AI_client_interaction})
#Generate a response for the AI client interaction
def AI_client_interaction_response(AI_client_interaction):
    prompt = PromptTemplate(
        input_variables=['chat_history', 'AI_client_interaction'], template='''You are an AI assistant. Respond to the client's interaction as helpful and informative as possible.

{chat_history}
Client: {AI_client_interaction}
AI Assistant:'''
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="AI_client_interaction")
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
    AI_client_response = ""
elif AI_client_interaction:
    if 'chat_llm_chain' not in st.session_state:
        st.session_state.chat_llm_chain = AI_client_interaction_response(AI_client_interaction)
    AI_client_response = st.session_state.chat_llm_chain.run(AI_client_interaction=AI_client_interaction)
else:
    AI_client_response = ""
#Display the AI client response to the user
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in AI_client_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
#Get CLE interests from the user
CLE_interests = st.multiselect("Select your CLE interests", ["Business Law", "Criminal Law", "Family Law", "Intellectual Property", "International Law", "Labor Law", "Real Estate Law"])
#Recommend specific CLE courses or readings based on the lawyer's practice area and historical cases they’ve shown interest in
def CLECourseRecommender(CLE_interests):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to recommend Continuing Legal Education (CLE) courses or readings based on a lawyer's practice area and historical cases they've shown interest in."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """The lawyer's interests are: {CLE_interests}. Please recommend suitable CLE courses or readings."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(CLE_interests=CLE_interests)
    return result # returns string   


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    CLE_suggestions = ""
elif CLE_interests:
    CLE_suggestions = CLECourseRecommender(CLE_interests)
else:
    CLE_suggestions = ""
#Display the CLE suggestions to the user
if CLE_suggestions:
    st.write(CLE_suggestions)
#Get document for translation from the user
document_for_translation = st.file_uploader("Upload the document for translation")
#Get language for translation from the user
language_for_translation = st.text_input("Enter the language for translation")
#Translate the legal document into the specified language
def legalDocumentTranslator(document_for_translation,language_for_translation):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are a legal document translator. Your task is to translate the given document into the specified language."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please translate the following document into {language_for_translation}: '{document_for_translation}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(document_for_translation=document_for_translation, language_for_translation=language_for_translation)
    return result # returns string   


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    translated_document = ""
elif document_for_translation and language_for_translation:
    translated_document = legalDocumentTranslator(document_for_translation,language_for_translation)
else:
    translated_document = ""
#Display the translated document to the user
if translated_document:
    st.download_button(label="Download Translated Document", data=translated_document, file_name='Translated_Document.txt')
#Get legal database details from the user
legal_database_details = st.text_area("Enter legal database details")
#Connect to the legal database and fetch and analyze more detailed data
def legalDataAnalyzer(legal_database_details):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an assistant designed to connect to a legal database and fetch and analyze data. The details of the database are '{legal_database_details}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please connect to the database and fetch and analyze the data."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(legal_database_details=legal_database_details)
    return result # returns string   


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    legal_database_analysis = ""
elif legal_database_details:
    legal_database_analysis = legalDataAnalyzer(legal_database_details)
else:
    legal_database_analysis = ""
#Display the legal database analysis to the user
if legal_database_analysis:
    st.table(legal_database_analysis)
#Get ethical guidelines query from the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])

if ethical_guidelines_query := st.chat_input("Do you have any questions about our ethical guidelines?"):
    with st.chat_message("user"):
        st.markdown(ethical_guidelines_query)
    st.session_state.messages.append({"role": "user", "content": ethical_guidelines_query})
#Generate a reminder of relevant ethical guidelines based on the context of the query
def generateEthicalGuidelinesReminder(ethical_guidelines_query):
    prompt = PromptTemplate(
        input_variables=['chat_history', 'ethical_guidelines_query'], template='''You are an AI assistant. Your task is to generate a reminder of relevant ethical guidelines based on the context of the query.

{chat_history}
User: {ethical_guidelines_query}
AI Assistant:'''
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="ethical_guidelines_query")
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
    ethical_guidelines_reminder = ""
elif ethical_guidelines_query:
    if 'chat_llm_chain' not in st.session_state:
        st.session_state.chat_llm_chain = generateEthicalGuidelinesReminder(ethical_guidelines_query)
    ethical_guidelines_reminder = st.session_state.chat_llm_chain.run(ethical_guidelines_query=ethical_guidelines_query)
else:
    ethical_guidelines_reminder = ""
#Display the ethical guidelines reminder to the user
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in ethical_guidelines_reminder.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
