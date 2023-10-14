import os
import streamlit as st
import tempfile
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)
st.title('Money Master')
# Get openai_api_key
st.sidebar.markdown("""# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑
2. Fill out the form by selecting your preferences for expense tracking, budget alerts, investment opportunities, and financial goal setting.
3. Click the "Get Personalized Advice" button.
4. Wait for the AI assistant to generate personalized financial advice based on your preferences.
5. View the advice displayed below the form.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("💰Money Master is a personal finance advisor app that empowers users to take control of their finances. With features like expense tracking, budget alerts, investment opportunities, and financial goal setting, Money Master provides personalized advice to help users manage their money effectively and achieve their financial goals.")

# Copy and paste all the functions as is


def financialAdvisor(expense_tracking, budget_alerts, investment_opportunities, financial_goal_setting):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.5
    )
    system_template = """You are an AI assistant providing personalized financial advice based on user preferences."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Based on your preferences for expense tracking: {expense_tracking}, budget alerts: {budget_alerts}, investment opportunities: {investment_opportunities}, and financial goal setting: {financial_goal_setting}, here is some personalized advice for you."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(expense_tracking=expense_tracking, budget_alerts=budget_alerts,
                       investment_opportunities=investment_opportunities, financial_goal_setting=financial_goal_setting)
    return result  # returns string


# Create a form

with st.form(key='financial_advisor'):
    # Under the form, take all the user inputs
    expense_tracking = st.radio(
        "Do you want to track your expenses?", ["Yes", "No"])
    budget_alerts = st.checkbox("Enable budget alerts")
    investment_opportunities = st.radio(
        "Do you prefer high-risk or low-risk investment opportunities?", ["High-risk", "Low-risk"])
    financial_goal_setting = st.radio(
        "Do you prefer to set financial goals?", ["Yes", "No"])
    submit_button = st.form_submit_button(label='Get Personalized Advice')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Call the functions
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            advice = ""
        elif expense_tracking and budget_alerts and investment_opportunities and financial_goal_setting:
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                advice = financialAdvisor(
                    expense_tracking, budget_alerts, investment_opportunities, financial_goal_setting)
        else:
            advice = ""

        # Show the results
        if advice is not None and len(str(advice)) > 0:
            # Under the st.form_submit_button, show the results.
            st.write(advice)
# END OF THE CODE
