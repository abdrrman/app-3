import os
import streamlit as st
import tempfile
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)
st.title('ZzzMaster: Sleep Like a Pro!')
# Get openai_api_key
st.sidebar.markdown("""# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑
2. Fill in the form with the required inputs:
   - Enter sleep data using the slider.
   - Select bedtime routines from the provided options.
   - Select ambient soundscapes from the provided options.
   - Choose whether you want sleep pattern analysis.
   - Enter personalized tips for sleep hygiene.
3. Click on the "Analyze Sleep" button to submit the form.
4. Wait for the analysis to complete (usually takes less than 10 seconds).
5. The results will be displayed below the form.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("ZzzMaster: Sleep Like a Pro! is an app that utilizes LLM technology to analyze sleep patterns and personal habits. With features such as sleep tracking, bedtime routines, ambient soundscapes, and sleep pattern analysis, it provides insights and recommendations for achieving optimal sleep quality and enhancing overall well-being. Get personalized tips for sleep hygiene and improve your sleep with ZzzMaster!")

# Copy and paste all the functions as is


def sleepAnalyzer(sleep_data, bedtime_routines, ambient_soundscapes, sleep_pattern_analysis, personalized_tips):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an AI assistant trained to analyze sleep patterns and personal habits using LLM (Long-term Lifestyle Monitoring). The provided inputs are: {sleep_data}, {bedtime_routines}, {ambient_soundscapes}, {sleep_pattern_analysis}, and {personalized_tips}."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Please analyze the provided sleep data, bedtime routines, ambient soundscapes, and perform sleep pattern analysis. Additionally, provide personalized tips based on the analysis. The inputs required for analysis are: {sleep_data}, {bedtime_routines}, {ambient_soundscapes}, {sleep_pattern_analysis}, and {personalized_tips}."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(sleep_data=sleep_data, bedtime_routines=bedtime_routines, ambient_soundscapes=ambient_soundscapes,
                       sleep_pattern_analysis=sleep_pattern_analysis, personalized_tips=personalized_tips)
    return result  # returns string


# Create a form

with st.form(key='sleep_analysis'):
    # Under the form, take all the user inputs
    sleep_data = st.slider("Enter sleep data", 0, 10, 5)
    bedtime_routines = st.multiselect("Select bedtime routines", [
                                      "Brushing teeth", "Reading a book", "Taking a bath", "Listening to music", "Meditating"])
    ambient_soundscapes = st.multiselect("Select ambient soundscapes", [
                                         "Forest", "Beach", "Rain", "Cafe", "City"])
    sleep_pattern_analysis = st.radio(
        "Do you want sleep pattern analysis?", ["Yes", "No"])
    personalized_tips = st.text_area(
        "Enter personalized tips for sleep hygiene")
    submit_button = st.form_submit_button(label='Analyze Sleep')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Call the functions
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            analysis_result = ""
        elif sleep_data and bedtime_routines and ambient_soundscapes and sleep_pattern_analysis and personalized_tips:
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                analysis_result = sleepAnalyzer(
                    sleep_data, bedtime_routines, ambient_soundscapes, sleep_pattern_analysis, personalized_tips)
        else:
            analysis_result = ""

        # Show the results
        if analysis_result is not None and len(str(analysis_result)) > 0:
            # Under the st.form_submit_button, show the results.
            st.write(analysis_result)
# END OF THE CODE