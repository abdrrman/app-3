
import time
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import streamlit as st
import tempfile

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.markdown("""# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑
2. Run the app code provided.
3. Type your message or question in the chat interface.
4. Wait for the response from the Elon Musk clone.
5. The response will be displayed in the chat interface.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("🚀Elons Mini-Me Chat is an innovative app that allows you to chat with a virtual clone of Elon Musk. With this app, you can engage in conversations, ask questions, and even get accurate answers from the virtual Elon Musk. Experience the thrill of interacting with one of the greatest minds of our time and explore the world of technology and innovation like never before.")

st.title('Elons Mini-Me Chat')
# Get message or question from the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if message := st.chat_input("Type your message or question"):
    with st.chat_message("user"):
        st.markdown(message)
    st.session_state.messages.append({"role": "user", "content": message})
# Generate the response or answer from Elon Musk clone based on the user input

msgs = StreamlitChatMessageHistory()

prompt = PromptTemplate(
    input_variables=['chat_history', 'message'], template='''You are an AI model trained to mimic Elon Musk's writing style and personality. Generate a response or answer based on the user input.

{chat_history}
User: {message}
Elon Musk Clone:'''
)
memory = ConversationBufferMemory(
    memory_key="chat_history", input_key="message", chat_memory=msgs, return_messages=True)
llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k",
                 openai_api_key=openai_api_key, temperature=0.7)
chat_llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=False,
    memory=memory,
)


if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    response = ""
elif message:
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        response = chat_llm_chain.run(message=message)
else:
    response = ""
# Display the response or answer to the user with chat interface

with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})
