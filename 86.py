from langchain.prompts.chat import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)
import os
import streamlit as st
import tempfile
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)  # Get openai_api_key
st.sidebar.markdown("""# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑
2. Fill in the name of the product in the "Enter the name of the product" text input.
3. Provide your comments about the product in the "Enter your comments" text area.
4. Click on the "Analyze Sentiments" button to analyze the sentiments.
5. Wait for the results to be generated (usually takes less than 10 seconds).
6. The generated textual snapshot of sentiments will be displayed below the button.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("Feel the Love! is an app that provides a quick textual snapshot of sentiments from user comments about different features of a product. It allows users to easily gauge the overall sentiment towards specific features and make informed decisions based on the feedback provided.")

# Copy and paste all the functions as is


def sentimentAnalyzer(product_name, user_comments):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an AI assistant tasked with generating a textual snapshot of sentiments from user comments about a product."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Please analyze the user comments '{user_comments}' about the product '{product_name}' and generate a textual snapshot of sentiments."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(product_name=product_name, user_comments=user_comments)
    return result  # returns string

# Create a form


with st.form(key='sentiment_analysis'):
    # Under the form, take all the user inputs
    st.title('Feel the Love!')
    # Get the name of the product from the user
    product_name = st.text_input("Enter the name of the product")
    # Get user comments about the product from the user
    user_comments = st.text_area("Enter your comments")
    submit_button = st.form_submit_button(label='Analyze Sentiments')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Call the functions
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            sentiment_snapshot = ""
        elif product_name and user_comments:
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                sentiment_snapshot = sentimentAnalyzer(
                    product_name, user_comments)
        else:
            sentiment_snapshot = ""

        # Show the results
        if sentiment_snapshot is not None and len(str(sentiment_snapshot)) > 0:
            # Under the st.form_submit_button, show the results.
            st.markdown(sentiment_snapshot)
# END OF THE CODE
