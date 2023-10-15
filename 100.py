import os
import streamlit as st
import tempfile
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)
st.title('Mindful Munchies')
# Get openai_api_key
st.sidebar.markdown("""# How to use

1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑
2. Select your nutrition goals from the provided options.
3. Select your dietary needs from the provided options.
4. Select your meal preferences from the provided options.
5. Select your hydration reminder preferences from the provided options.
6. Select your nutrient tracking preferences from the provided options.
7. Select your mindfulness exercises from the provided options.
8. Select your educational content preferences from the provided options.
9. Click the "Submit" button.
10. Wait for the personalized meal suggestions to be generated.
11. View the personalized meal suggestions.
12. View the hydration reminders.
13. View the nutrient tracking information.
14. View the mindfulness exercises.
15. View the educational content on food and nutrition.""")
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
st.sidebar.markdown("# About")
st.sidebar.markdown("🍽️Mindful Munchies is an app designed to help you develop a mindful eating practice. With personalized meal suggestions, hydration reminders, and nutrient tracking, it offers guidance on nutrition and conscious food consumption tailored to your health goals and dietary needs. The app also provides mindfulness exercises during meals and educational content on food and nutrition to support your journey towards a healthier lifestyle.")

# Copy and paste all the functions as is


def mealSuggestionGenerator(nutrition_goals, dietary_needs, meal_preferences):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are a personalized meal suggestion assistant. Your task is to generate meal suggestions based on the user's nutrition goals, dietary needs, and meal preferences."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        system_template)
    human_template = """Please generate personalized meal suggestions based on the following inputs:
- Nutrition goals: {nutrition_goals}
- Dietary needs: {dietary_needs}
- Meal preferences: {meal_preferences}"""
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(nutrition_goals=nutrition_goals,
                       dietary_needs=dietary_needs, meal_preferences=meal_preferences)
    return result  # returns string

# Create a form


with st.form(key='mindful_munchies'):
    # Under the form, take all the user inputs
    nutrition_goals = st.multiselect("Select your nutrition goals", [
                                     "Weight loss", "Muscle gain", "Healthy eating", "Improved digestion"])
    dietary_needs = st.multiselect("Select your dietary needs", [
                                   "Vegetarian", "Vegan", "Gluten-free", "Dairy-free"])
    meal_preferences = st.multiselect("Select your meal preferences", [
                                      "Vegetarian", "Vegan", "Gluten-free", "Dairy-free"])
    hydration_reminders = st.multiselect("Select your hydration reminder preferences", [
                                         "Every hour", "Every 2 hours", "Every 3 hours", "Every 4 hours"])
    nutrient_tracking = st.multiselect("Select nutrient tracking preferences", [
                                       "Calories", "Protein", "Carbohydrates", "Fat", "Vitamins", "Minerals"])
    mindfulness_exercises = st.multiselect("Select your mindfulness exercises", [
                                           "Meditation", "Breathing exercises", "Yoga", "Walking", "Journaling"])
    educational_content = st.multiselect("Select educational content preferences", [
                                         "Science", "Math", "History", "Language", "Art"])
    submit_button = st.form_submit_button(label='Submit')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Call the functions
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            personalized_meal_suggestions = ""
        elif nutrition_goals and dietary_needs and meal_preferences:
            with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
                personalized_meal_suggestions = mealSuggestionGenerator(
                    nutrition_goals, dietary_needs, meal_preferences)
        else:
            personalized_meal_suggestions = ""

        # Show the results
        # Display the personalized meal suggestions to the user
        if personalized_meal_suggestions is not None and len(str(personalized_meal_suggestions)) > 0:
            # Under the st.form_submit_button, show the results.
            st.write(personalized_meal_suggestions)

        # Display the hydration reminders to the user
        if hydration_reminders is not None and len(str(hydration_reminders)) > 0:
            # Under the st.form_submit_button, show the results.
            st.markdown(hydration_reminders)

        # Display the nutrient tracking information to the user
        if nutrient_tracking is not None and len(str(nutrient_tracking)) > 0:
            # Under the st.form_submit_button, show the results.
            st.write(nutrient_tracking)

        # Display the mindfulness exercises to the user
        if mindfulness_exercises is not None and len(str(mindfulness_exercises)) > 0:
            # Under the st.form_submit_button, show the results.
            st.markdown(mindfulness_exercises)

        # Display the educational content on food and nutrition to the user
        if educational_content is not None and len(str(educational_content)) > 0:
            # Under the st.form_submit_button, show the results.
            st.markdown(educational_content)
# END OF THE CODE