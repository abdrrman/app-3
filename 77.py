import os
import streamlit as st
import tempfile
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)
st.title('glip')
os.environ['SERPER_API_KEY'] = 'ad9a1ff593f1ff9ae87881611f65c78182355d92'
# Get openai_api_key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

# Copy and paste all the functions as is


def promptTemplateGenerator(input_text, model_name, temperature, max_tokens):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an AI assistant that generates prompt templates based on the given input text, model name, temperature, and maximum tokens."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Create a prompt template using the input text: '{input_text}', model name: '{model_name}', temperature: {temperature}, and maximum tokens: {max_tokens}."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(input_text=input_text, model_name=model_name,
                       temperature=temperature, max_tokens=max_tokens)
    return result  # returns string


def jsonGenerator(prompt):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an AI assistant that generates structured JSON objects based on a given {prompt}."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Please use the {prompt} template to generate the structured JSON object."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(prompt=prompt)
    return result  # returns string

# Create a form


with st.form(key='story_game'):
    # Under the form, take all the user inputs
    input_text = st.text_area("Enter the input text")
    model_name = st.text_input("Enter the model name")
    temperature = st.number_input("Enter the temperature value")
    max_tokens = st.number_input("Enter the maximum tokens value")
    submit_button = st.form_submit_button(label='Submit Story')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Call the functions
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            prompt = ""
        elif input_text and model_name and temperature and max_tokens:
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                prompt = promptTemplateGenerator(
                    input_text, model_name, temperature, max_tokens)
        else:
            prompt = ""

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            json_object = ""
        elif prompt:
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                json_object = jsonGenerator(prompt)
        else:
            json_object = ""

        # Show the results
        if json_object is not None and len(str(json_object)) > 0:
            # Under the st.form_submit_button, show the results.
            st.write(json_object)

# END OF THE CODE
