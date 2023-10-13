import os
import streamlit as st
import tempfile
st.title('Unbelievable App!')
# Get openai_api_key
st.sidebar.markdown("""# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑

2. Fill in the "Enter the overview of the system" text area with the desired overview.

3. Click the "Submit" button.

4. The overview will be displayed below the submit button.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("Unbelievable App! is a powerful application that offers a wide range of features to enhance your productivity and simplify your daily tasks. With its intuitive interface and advanced functionality, this app is designed to revolutionize the way you work. Whether you need to manage your schedule, collaborate with team members, or stay organized, Unbelievable App! has got you covered. Say goodbye to endless paperwork and hello to a more efficient and streamlined workflow.")

# Copy and paste all the functions as is


def foo1():
    result = "res"
    return result

# Create a form


with st.form(key='unbelievable_app'):
    # Under the form, take all the user inputs
    overview = st.text_area("Enter the overview of the system")
    submit_button = st.form_submit_button(label='Submit')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Call the functions
        if overview is not None and len(str(overview)) > 0:
            st.markdown(overview)

        # Show the results
        if overview is not None and len(str(overview)) > 0:
            # Under the st.form_submit_button, show the results.
            st.markdown(overview)
# END OF THE CODE
