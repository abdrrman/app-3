
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

st.title('ParaLegal AI')
#Get case law or legal judgment from the user
case_law_or_legal_judgment = st.text_area("Enter case law or legal judgment")
#Summarize the given case law or legal judgment
def legalSummarizer(case_law_or_legal_judgment):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are a legal assistant, and your task is to summarize the given case law or legal judgment."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """The case law or legal judgment is: '{case_law_or_legal_judgment}'. Please provide a concise summary."""
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
#Get context for draft from the user
context_for_draft = st.text_area("Enter context for draft")
#Generate a draft for the given legal document type and context
def legalDraftGenerator(legal_document_type,context_for_draft):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are a legal assistant tasked with drafting a {legal_document_type} based on the provided context."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """The type of legal document is a {legal_document_type} and the context is '{context_for_draft}'. Please generate a draft for this document."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(legal_document_type=legal_document_type, context_for_draft=context_for_draft)
    return result # returns string   


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    draft = ""
elif legal_document_type and context_for_draft:
    draft = legalDraftGenerator(legal_document_type,context_for_draft)
else:
    draft = ""
#Display the generated draft to the user
if draft:
    st.text(draft)
#Get legal query from the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])

if legal_query := st.chat_input("Enter your legal query"):
    with st.chat_message("user"):
        st.markdown(legal_query)
    st.session_state.messages.append({"role": "user", "content": legal_query})
#Generate the response for the legal query
def legalQueryResponse(legal_query):
    prompt = PromptTemplate(
        input_variables=['chat_history', 'legal_query'], template='''You are a legal advisor. Respond to the legal query as accurately and professionally as possible.

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
        st.session_state.chat_llm_chain = legalQueryResponse(legal_query)
    legal_response = st.session_state.chat_llm_chain.run(legal_query=legal_query)
else:
    legal_response = ""
#Display the response for the legal query to the user
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
    human_template = """Please analyze the evolution of legal principles based on the following historical legal decisions: '{historical_legal_decisions}'."""
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
#Get area of practice from the user
area_of_practice = st.text_input("Enter your area of practice")
#Generate a news feed tailored to the user's specific area of practice
def newsFeedGenerator(area_of_practice):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are a news feed generator, tasked with creating a news feed tailored to the user's specific area of practice: '{area_of_practice}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please generate a news feed related to the area of practice: {area_of_practice}."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(area_of_practice=area_of_practice)
    return result # returns string   


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    news_digest = ""
elif area_of_practice:
    news_digest = newsFeedGenerator(area_of_practice)
else:
    news_digest = ""
#Display the news digest to the user
if news_digest:
    st.write(news_digest)
#Get client interaction scenario from the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])

if client_interaction_scenario := st.chat_input("Describe the client interaction scenario"):
    with st.chat_message("user"):
        st.markdown(client_interaction_scenario)
    st.session_state.messages.append({"role": "user", "content": client_interaction_scenario})
#Generate the response for the client interaction scenario
def clientInteractionResponse(client_interaction_scenario):
    prompt = PromptTemplate(
        input_variables=['chat_history', 'client_interaction_scenario'], template='''You are a customer service representative. Respond to the client interaction scenario as professionally as possible.

Scenario: {client_interaction_scenario}

Customer Service Representative:'''
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="client_interaction_scenario")
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
    client_interaction_response = ""
elif client_interaction_scenario:
    if 'chat_llm_chain' not in st.session_state:
        st.session_state.chat_llm_chain = clientInteractionResponse(client_interaction_scenario)
    client_interaction_response = st.session_state.chat_llm_chain.run(client_interaction_scenario=client_interaction_scenario)
else:
    client_interaction_response = ""
#Display the response for the client interaction scenario to the user
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in client_interaction_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
#Get practice area from the user
practice_area = st.text_input("Enter your practice area")
#Get interest in cases from the user
interest_in_cases = st.selectbox("Are you interested in cases?", ["Yes", "No"])
#Recommend specific CLE courses or readings based on the lawyer's practice area and historical cases they’ve shown interest in
def CLECourseRecommender(practice_area,interest_in_cases):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to recommend Continuing Legal Education (CLE) courses or readings based on a lawyer's practice area and the historical cases they've shown interest in."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """The lawyer's practice area is {practice_area} and they have shown interest in {interest_in_cases}. Please recommend appropriate CLE courses or readings."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(practice_area=practice_area, interest_in_cases=interest_in_cases)
    return result # returns string   


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    cle_suggestions = ""
elif practice_area and interest_in_cases:
    cle_suggestions = CLECourseRecommender(practice_area,interest_in_cases)
else:
    cle_suggestions = ""
#Display the CLE suggestions to the user
if cle_suggestions:
    st.write(cle_suggestions)
#Get document for translation from the user
document_for_translation = st.file_uploader("Upload the document for translation")
#Get language for translation from the user
language_for_translation = st.text_input("Enter the language for translation")
#Translate the document into the specified language
def documentTranslator(document_for_translation,language_for_translation):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are a language translator. Your task is to translate a document into the specified language."""
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
    translated_document = documentTranslator(document_for_translation,language_for_translation)
else:
    translated_document = ""
#Display the translated document to the user
if translated_document:
    st.download_button(label="Download Translated Document", data=translated_document, file_name='Translated_Document.txt')
#Get legal database details from the user
legal_database_details = st.text_area("Enter legal database details")
#Fetch and analyze more detailed data from the legal database
def legalDataAnalyzer(legal_database_details):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an assistant designed to fetch and analyze data from a legal database."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please fetch and analyze the following details from the legal database: '{legal_database_details}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(legal_database_details=legal_database_details)
    return result # returns string   


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    database_analysis = ""
elif legal_database_details:
    database_analysis = legalDataAnalyzer(legal_database_details)
else:
    database_analysis = ""
#Display the database analysis to the user
if database_analysis:
    st.write(database_analysis)
#Get ethical query from the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])

if ethical_query := st.chat_input("Enter your ethical query"):
    with st.chat_message("user"):
        st.markdown(ethical_query)
    st.session_state.messages.append({"role": "user", "content": ethical_query})
#Generate the response for the ethical query
def respondEthicalQuery(ethical_query):
    prompt = PromptTemplate(
        input_variables=['chat_history', 'ethical_query'], template='''You are an AI ethics expert. Respond to the ethical query raised by the user.

{chat_history}
User: {ethical_query}
Ethics Expert:'''
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="ethical_query")
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
    ethical_response = ""
elif ethical_query:
    if 'chat_llm_chain' not in st.session_state:
        st.session_state.chat_llm_chain = respondEthicalQuery(ethical_query)
    ethical_response = st.session_state.chat_llm_chain.run(ethical_query=ethical_query)
else:
    ethical_response = ""
#Display the response for the ethical query to the user
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in ethical_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
