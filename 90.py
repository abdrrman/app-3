import os
import streamlit as st
import tempfile
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)
st.title('Magic Menu Maker')
# Get openai_api_key
st.sidebar.markdown("""# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑
2. Fill in the list of ingredients in the text area.
3. Select the dietary restrictions from the provided options.
4. Select any allergies from the provided options.
5. Click on the "Generate Recipe" button.
6. Wait for the recipe to be generated (usually takes less than 10 seconds).
7. The generated recipe will be displayed below the button.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("Magic Menu Maker is a customized recipe generator app designed for food enthusiasts and home cooks. With Magic Menu Maker, you can easily generate recipes based on the ingredients you have available at home or your dietary restrictions and allergies. The app also provides nutritional information for each recipe, suggests alternative ingredients, and offers cooking tips to help you create delicious meals.")

# Copy and paste all the functions as is


def recipeGenerator(ingredients, dietary_restrictions, allergies):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.5
    )
    system_template = """You are a recipe generator. Your task is to create a recipe based on the given inputs."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Please create a recipe using the following ingredients: {ingredients}. The recipe should accommodate the dietary restrictions: {dietary_restrictions} and avoid any allergies: {allergies}."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(ingredients=ingredients,
                       dietary_restrictions=dietary_restrictions, allergies=allergies)
    return result  # returns string


# Create a form

with st.form(key='recipe_generator'):
    # Under the form, take all the user inputs
    ingredients = st.text_area("Enter the list of ingredients")
    dietary_restrictions = st.multiselect("Select dietary restrictions", [
                                          "Vegetarian", "Vegan", "Gluten-free", "Dairy-free"])
    allergies = st.multiselect(
        "Select allergies", ["Peanuts", "Shellfish", "Dairy", "Gluten", "Eggs"])
    submit_button = st.form_submit_button(label='Generate Recipe')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Call the functions
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            recipe = ""
        elif ingredients and dietary_restrictions and allergies:
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                recipe = recipeGenerator(
                    ingredients, dietary_restrictions, allergies)
        else:
            recipe = ""

        # Show the results
        if recipe is not None and len(str(recipe)) > 0:
            # Under the st.form_submit_button, show the results.
            st.write(recipe)
# END OF THE CODE