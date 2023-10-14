import os
import streamlit as st
import tempfile
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)
st.title('Event Bliss')
# Get openai_api_key
st.sidebar.markdown("""# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑
2. Fill in the guest list, budget, and timeline in the form.
3. Click on the "Generate Event Plan" button.
4. Wait for the event plan to be generated (usually takes less than 10 seconds).
5. The generated event plan will be displayed below the button.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("Event Bliss is an intuitive event planning app that helps users effortlessly manage guests, budgets, and timelines. With its user-friendly interface, you can easily create and organize guest lists, track expenses, and set reminders for important tasks. Whether you're planning a small gathering or a large-scale event, Event Bliss is your go-to assistant for a stress-free planning experience.")

# Copy and paste all the functions as is


def eventPlanner(guest_list, budget, timeline):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an event planner. Your task is to create an event plan based on the given guest list, budget, and timeline."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Please create an event plan using the following inputs:
Guest List: {guest_list}
Budget: {budget}
Timeline: {timeline}"""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(guest_list=guest_list, budget=budget, timeline=timeline)
    return result  # returns string


# Create a form

with st.form(key='event_planner'):
    # Under the form, take all the user inputs
    guest_list = st.text_area("Enter the guest list")
    budget = st.number_input("Enter the budget")
    timeline = st.slider("Select the timeline",
                         min_value=0, max_value=100, step=1)
    submit_button = st.form_submit_button(label='Generate Event Plan')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Call the functions
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            event_plan = ""
        elif guest_list and budget and timeline:
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                event_plan = eventPlanner(guest_list, budget, timeline)
        else:
            event_plan = ""

        # Show the results
        if event_plan is not None and len(str(event_plan)) > 0:
            # Under the st.form_submit_button, show the results.
            st.write(event_plan)
# END OF THE CODE
