import os
import streamlit as st
import tempfile
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)
st.title('Time Savior')
# Get openai_api_key
st.sidebar.markdown("""# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑
2. Fill in the task, preferred focus technique, enable break reminders, and choose whether to receive productivity reports.
3. Click on the "Get Productivity Suggestions" button.
4. Wait for the suggestions to be generated (usually takes less than 10 seconds).
5. The suggestions will be displayed below the button.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("🕒Time Savior is a productivity coach app that analyzes your behavior and provides personalized techniques to help you manage your time and tasks effectively. With features like task management, focus techniques, break reminders, and productivity reports, Time Savior is your ultimate tool for boosting productivity and achieving your goals.")

# Copy and paste all the functions as is


def productivityAnalyzer(task, focus_technique, break_reminder, productivity_report):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an AI assistant designed to analyze the user's inputs and generate personalized productivity suggestions."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Based on the user's inputs: task = '{task}', focus technique = '{focus_technique}', break reminder = '{break_reminder}', and productivity report = '{productivity_report}', please provide personalized productivity suggestions."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(task=task, focus_technique=focus_technique,
                       break_reminder=break_reminder, productivity_report=productivity_report)
    return result  # returns string


# Create a form

with st.form(key='time_savior'):
    # Under the form, take all the user inputs
    task = st.text_input("Enter your task")
    focus_technique = st.radio("Select your preferred focus technique", [
                               "Highlight", "Underline", "Bold", "Italic"])
    break_reminder = st.checkbox("Enable break reminders")
    productivity_report = st.checkbox(
        "Do you want to receive productivity reports?")
    submit_button = st.form_submit_button(label='Get Productivity Suggestions')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Call the functions
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            suggestions = ""
        elif task and focus_technique and break_reminder and productivity_report:
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                suggestions = productivityAnalyzer(
                    task, focus_technique, break_reminder, productivity_report)
        else:
            suggestions = ""

        # Show the results
        if suggestions is not None and len(str(suggestions)) > 0:
            # Under the st.form_submit_button, show the results.
            st.write(suggestions)
# END OF THE CODE