import os
import streamlit as st
import tempfile
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)
st.title('Workaholics Paradise')
# Get openai_api_key
st.sidebar.markdown("""# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑
2. Fill out the form with your preferences:
   - Choose whether you want ergonomic setup advice.
   - Enable or disable productivity analytics.
   - Choose whether you prefer virtual coworking spaces.
   - Choose whether you prefer mental wellness checks.
3. Click on the "Generate App Experience" button.
4. Wait for the app to generate a personalized app experience based on your preferences.
5. The generated app experience will be displayed below the form.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("🏠Workaholics Paradise is a productivity app designed to support remote workers in maintaining a healthy work-life balance and optimizing their home office environment. With features such as ergonomic setup advice, productivity analytics, virtual coworking spaces, and mental wellness checks, this app aims to enhance productivity, well-being, and efficiency for remote workers.")

# Copy and paste all the functions as is


def appExperienceGenerator(ergonomic_setup, productivity_analytics, virtual_coworking_spaces, mental_wellness_checks):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an AI assistant tasked with generating a personalized app experience for the user based on their preferences."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Please create a personalized app experience for the user based on their preferences. The user prefers an ergonomic setup: {ergonomic_setup}, utilizes productivity analytics: {productivity_analytics}, enjoys virtual coworking spaces: {virtual_coworking_spaces}, and values mental wellness checks: {mental_wellness_checks}."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(ergonomic_setup=ergonomic_setup, productivity_analytics=productivity_analytics,
                       virtual_coworking_spaces=virtual_coworking_spaces, mental_wellness_checks=mental_wellness_checks)
    return result  # returns string

# Create a form


with st.form(key='app_experience_form'):
    # Under the form, take all the user inputs
    ergonomic_setup = st.radio(
        "Do you want ergonomic setup advice?", ["Yes", "No"])
    productivity_analytics = st.checkbox("Enable productivity analytics")
    virtual_coworking_spaces = st.radio(
        "Do you prefer virtual coworking spaces?", ["Yes", "No"])
    mental_wellness_checks = st.radio(
        "Do you prefer mental wellness checks?", ["Yes", "No"])
    submit_button = st.form_submit_button(label='Generate App Experience')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Call the functions
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            app_experience = ""
        elif ergonomic_setup and virtual_coworking_spaces and mental_wellness_checks:
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                app_experience = appExperienceGenerator(
                    ergonomic_setup, productivity_analytics, virtual_coworking_spaces, mental_wellness_checks)
        else:
            app_experience = ""

        # Show the results
        if app_experience is not None and len(str(app_experience)) > 0:
            # Under the st.form_submit_button, show the results.
            st.write(app_experience)
# END OF THE CODE