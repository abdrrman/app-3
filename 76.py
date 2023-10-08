
import time
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import streamlit as st
import tempfile

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

st.title('AI Workers for Hire')
os.environ['SERPER_API_KEY'] = 'ad9a1ff593f1ff9ae87881611f65c78182355d92'
# Get message from the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if message := st.chat_input("Type your message"):
    with st.chat_message("user"):
        st.markdown(message)
    st.session_state.messages.append({"role": "user", "content": message})
# Generate the response coming from the hivemind AI personal assistant


def hivemind_ai_response(message):
    prompt = PromptTemplate(
        input_variables=['chat_history', 'message'], template='''You are a hivemind AI personal assistant. Respond to the user's message as helpful and informative as possible.

{chat_history}
User: {message}
Hivemind AI:'''
    )
    memory = ConversationBufferMemory(
        memory_key="chat_history", input_key="message")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k",
                     openai_api_key=openai_api_key, temperature=0.5)
    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )
    return chat_llm_chain


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    ai_response = ""
elif message:
    if 'chat_llm_chain' not in st.session_state:
        st.session_state.chat_llm_chain = hivemind_ai_response(message)
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        ai_response = st.session_state.chat_llm_chain.run(message=message)
else:
    ai_response = ""
# Display the AI's response to the user

with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in ai_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})
