
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
2. Run the provided code.
3. Input your message in the chat interface.
4. Wait for the AI-generated response.
5. View the generated response in the chat interface.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("ElonBot is an AI-powered replica of Elon Musk that can answer your questions with a touch of humor. With its question answering feature, you can ask ElonBot anything and receive accurate answers, complete with emojis to add a fun twist to the conversation. Get ready to have a laugh while gaining knowledge with ElonBot!")

st.title('ElonBot: 🤔+😂 AI Replica')
# Get user input for the chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Type your message"):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
# Generate a response based on the user's input

msgs = StreamlitChatMessageHistory()

prompt = PromptTemplate(
    input_variables=['chat_history', 'user_input'], template='''You are a chatbot. Generate a response based on the user's input.

{chat_history}
User: {user_input}
Chatbot:'''
)
memory = ConversationBufferMemory(
    memory_key="chat_history", input_key="user_input", chat_memory=msgs, return_messages=True)
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
elif user_input:
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        response = chat_llm_chain.run(user_input=user_input)
else:
    response = ""
# Display the generated response to the user

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
