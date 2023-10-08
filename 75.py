import os
import streamlit as st
import tempfile
from langchain.chat_models import ChatOpenAI
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
from langchain.llms import OpenAI
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents.tools import Tool
from langchain.chains import LLMMathChain
st.title('Age Finder')
os.environ['SERPER_API_KEY'] = st.secrets.get('SERPER_API_KEY', '')
# Get openai_api_key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

# Copy and paste all the functions as is


def find_celebrity_age(celebrity_name):
    search_input = "Find the age of the celebrity {celebrity_name} on the internet.".format(
        celebrity_name=celebrity_name)
    search = GoogleSerperAPIWrapper()
    llm = OpenAI(temperature=0)
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events"
        ),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math"
        ),
    ]
    model = ChatOpenAI(temperature=0, model_name="gpt-4")
    planner = load_chat_planner(model)
    executor = load_agent_executor(model, tools, verbose=True)
    agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)
    try:
        with st.spinner('DemoGPT is working on it. It might take 1-2 minutes...'):
            return agent.run(search_input)
    except AuthenticationError:
        st.warning(
            'This tool requires GPT-4. Please enter a key that has GPT-4 access', icon="⚠️")
        return ''

# Create a form


with st.form(key='age_finder'):
    # Under the form, take all the user inputs
	celebrity_name = st.text_input("Enter the name of the celebrity")
	submit_button = st.form_submit_button(label='Find Celebrity Age')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        ######## Call the functions
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            celebrity_age = ""
        elif celebrity_name:
            celebrity_age = find_celebrity_age(celebrity_name)
        else:
            celebrity_age = ""
        
        ######## Show the results
        if celebrity_age is not None and len(str(celebrity_age)) > 0:
            #Under the st.form_submit_button, show the results.
            st.write("The celebrity is", celebrity_age, "years old")
############################################################# END OF THE CODE