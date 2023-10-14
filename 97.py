import os
import streamlit as st
import tempfile
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.chains import LLMMathChain
from langchain.callbacks import StreamlitCallbackHandler  # Get openai_api_key
st.sidebar.markdown("""# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑
2. Fill in your location and select the type of emergency in the form.
3. Click the "Submit Story" button.
4. Wait for the results to load.
5. View the generated real-time alerts, resource maps, and direct lines to emergency services under the form.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("🚨Crisis Savior is a powerful app designed to assist users during times of crisis, such as natural disasters and pandemics. With real-time information, emergency procedures, communication tools, and essential resource locators, this app ensures that users have the necessary tools to navigate through challenging situations. Stay informed with real-time alerts, access resource maps, perform safety check-ins, and connect directly with emergency services. Be prepared and stay safe with Crisis Savior.")

# Copy and paste all the functions as is


def combineStrings(user_location, emergency_type):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an assistant tasked with combining the user's location and emergency type into a single string."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """The user's location is {user_location} and the emergency type is {emergency_type}. Please combine them into a single string."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(user_location=user_location,
                       emergency_type=emergency_type)
    return result  # returns string


def generate_real_time_alerts(combined_info):
    search_input = "Generate real-time alerts for the specified emergency type and user location: {combined_info}".format(
        combined_info=combined_info)
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0)
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    tools = [
        DuckDuckGoSearchRun(name="Search"),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math"
        ),
    ]
    model = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)
    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
    return agent.run(search_input, callbacks=[st_cb])


def generate_resource_maps(combined_info):
    search_input = "Generate resource maps for the specified emergency type and user location: {combined_info}".format(
        combined_info=combined_info)
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0)
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    tools = [
        DuckDuckGoSearchRun(name="Search"),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math"
        ),
    ]
    model = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)
    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
    return agent.run(search_input, callbacks=[st_cb])


def generate_emergency_services(combined_info):
    search_input = "Generate direct lines to emergency services for the specified emergency type and user location: {combined_info}".format(
        combined_info=combined_info)
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0)
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    tools = [
        DuckDuckGoSearchRun(name="Search"),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math"
        ),
    ]
    model = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)
    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
    return agent.run(search_input, callbacks=[st_cb])

# Create a form


with st.form(key='story_game'):
    # Under the form, take all the user inputs
    st.title('Crisis Savior')
    # Get the user's location
    user_location = st.text_input("Enter your location")
    # Get the type of emergency
    emergency_type = st.selectbox("Select the type of emergency", [
                                  "Fire", "Medical", "Natural Disaster", "Accident", "Other"])
    submit_button = st.form_submit_button(label='Submit Story')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Call the functions
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            combined_info = ""
        elif user_location and emergency_type:
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                combined_info = combineStrings(user_location, emergency_type)
        else:
            combined_info = ""

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            alerts = ""
        elif combined_info:
            alerts = generate_real_time_alerts(combined_info)
        else:
            alerts = ''

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            resource_maps = ""
        elif combined_info:
            resource_maps = generate_resource_maps(combined_info)
        else:
            resource_maps = ''

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            emergency_services = ""
        elif combined_info:
            emergency_services = generate_emergency_services(combined_info)
        else:
            emergency_services = ''

        # Show the results
        if alerts is not None and len(str(alerts)) > 0:
            # Under the st.form_submit_button, show the results.
            st.info(alerts)

        if resource_maps is not None and len(str(resource_maps)) > 0:
            # Under the st.form_submit_button, show the results.
            st.write(resource_maps)

        if emergency_services is not None and len(str(emergency_services)) > 0:
            # Under the st.form_submit_button, show the results.
            st.write(emergency_services)