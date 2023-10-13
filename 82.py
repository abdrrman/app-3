import os
import streamlit as st
import tempfile
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)
st.title('Gym Buddy')
# Get openai_api_key
st.sidebar.markdown("""# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑
2. Fill in the user's goals in the text area.
3. Click on the "Generate Fitness Routine" button.
4. Wait for the fitness routine to be generated (takes less than 10 seconds).
5. The generated fitness routine will be displayed below the button.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("Gym God is a fitness app that provides personalized workout routines based on your fitness goals. Whether you want to build muscle, lose weight, or improve your overall fitness, Gym God will recommend the perfect routine for you.")

# Copy and paste all the functions as is


def fitnessRoutineGenerator(user_goals):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.5
    )
    system_template = """You are a fitness assistant. Your task is to generate a fitness routine based on the user's goals: {user_goals}."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Please generate a fitness routine tailored to the user's goals: {user_goals}."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(user_goals=user_goals)
    return result  # returns string

# Create a form


with st.form(key='fitness_routine_form'):
    # Under the form, take all the user inputs
    user_goals = st.text_area("Enter user's goals")
    submit_button = st.form_submit_button(label='Generate Fitness Routine')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Call the functions
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            fitness_routine = ""
        elif user_goals:
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                fitness_routine = fitnessRoutineGenerator(user_goals)
        else:
            fitness_routine = ""

        # Show the results
        if fitness_routine is not None and len(str(fitness_routine)) > 0:
            # Under the st.form_submit_button, show the results.
            st.markdown(fitness_routine)
# END OF THE CODE
