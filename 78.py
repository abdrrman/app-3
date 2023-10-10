import os
import streamlit as st
import tempfile
st.title('book')
os.environ['SERPER_API_KEY'] = 'ad9a1ff593f1ff9ae87881611f65c78182355d92'
# Get openai_api_key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

# Copy and paste all the functions as is


def foo1():
    result = "res"
    return result


def foo2(half_story, user_choice):
    result = half_story + user_choice
    return result

# Create a form


with st.form(key='book_details'):
    # Under the form, take all the user inputs
    # Get the title of the book from the user
    book_title = st.text_input("Enter the title of the book")
    # Get the author of the book from the user
    book_author = st.text_input("Enter the author of the book")
    # Get the price of the book from the user
    book_price = st.number_input("Enter the price of the book")
    # Get the condition of the book from the user
    book_condition = st.selectbox("Select the condition of the book", [
                                  "New", "Like New", "Good", "Fair", "Poor"])
    # Get the description of the book from the user
    book_description = st.text_area("Enter the description of the book")
    submit_button = st.form_submit_button(label='Submit Book Details')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Call the functions
        if book_title is not None and book_author is not None and book_price is not None and book_condition is not None and book_description is not None:
            st.header(book_title)
            st.subheader(f"Author: {book_author}")
            st.subheader(f"Price: {book_price}")
            st.subheader(f"Condition: {book_condition}")
            st.write(book_description)

# END OF THE CODE
