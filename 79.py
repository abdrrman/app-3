import os
import streamlit as st
import tempfile
import library1
import library2
import library3
st.title('test')
os.environ['SERPER_API_KEY'] = 'ad9a1ff593f1ff9ae87881611f65c78182355d92'
# Get openai_api_key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

# Copy and paste all the functions as is


def generate_test_question():
    # complete the function and return the result


def analyze_answer(question, answer):
    # complete the function and return the result

    # Create a form


with st.form(key='test_question_form'):
    # Under the form, take all the user inputs
    if openai_api_key is not None and len(openai_api_key) > 0:
        question = generate_test_question()
    else:
        question = ''
    # Display the test question to the user
    if question is not None and len(str(question)) > 0:
        st.header(question)
    # Get the user's answer to the test question
    answer = st.radio("What is the capital of France?", [
                      "Paris", "London", "Berlin", "Madrid"])
    submit_button = st.form_submit_button(label='Submit Answer')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Call the functions
        if question is not None and len(question) > 0 and answer is not None and len(answer) > 0:
            analysis = analyze_answer(question, answer)
        else:
            analysis = ''

        # Show the results
        if analysis is not None and len(str(analysis)) > 0:
            # Under the st.form_submit_button, show the results.
            st.write(analysis)
# END OF THE CODE
