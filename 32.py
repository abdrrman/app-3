import os
import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.document_loaders import *
from langchain.chains.summarize import load_summarize_chain
import tempfile
from langchain.docstore.document import Document
import time
from langchain.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

st.title('Hackla')

def websiteGenerator(header_image,cta_text,concept_intro,mission_statement,service_overview,customer_reviews,footer_links,language_selection,login_register,detailed_service_description,online_booking,booking_process_guide,faq,platform_history,team_intro,mission_vision,contact_form,contact_info,google_maps,social_media_login,user_dashboard,invoice_history,profile_settings,subscription_model,live_chat_support,search_function,tip_feature,rating_system,blog_posts):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are a website generator. Your task is to generate a website with the following features: header image, call to action text, concept introduction, mission statement, service overview, customer reviews, footer links, menu items, language selection, login/register, detailed service description, online booking, booking process guide, FAQ, platform history, team introduction, mission and vision, contact form, contact information, Google maps, social media login, user dashboard, invoice history, profile settings, subscription model, live chat support, search function, tip feature, rating system, and blog posts."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please generate a website with the following features: Header Image: {header_image}, CTA Text: {cta_text}, Concept Intro: {concept_intro}, Mission Statement: {mission_statement}, Service Overview: {service_overview}, Customer Reviews: {customer_reviews}, Footer Links: {footer_links}, Language Selection: {language_selection}, Login/Register: {login_register}, Detailed Service Description: {detailed_service_description}, Online Booking: {online_booking}, Booking Process Guide: {booking_process_guide}, FAQ: {faq}, Platform History: {platform_history}, Team Intro: {team_intro}, Mission and Vision: {mission_vision}, Contact Form: {contact_form}, Contact Info: {contact_info}, Google Maps: {google_maps}, Social Media Login: {social_media_login}, User Dashboard: {user_dashboard}, Invoice History: {invoice_history}, Profile Settings: {profile_settings}, Subscription Model: {subscription_model}, Live Chat Support: {live_chat_support}, Search Function: {search_function}, Tip Feature: {tip_feature}, Rating System: {rating_system}, Blog Posts: {blog_posts}."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(header_image=header_image, cta_text=cta_text, concept_intro=concept_intro, mission_statement=mission_statement, service_overview=service_overview, customer_reviews=customer_reviews, footer_links=footer_links, language_selection=language_selection, login_register=login_register, detailed_service_description=detailed_service_description, online_booking=online_booking, booking_process_guide=booking_process_guide, faq=faq, platform_history=platform_history, team_intro=team_intro, mission_vision=mission_vision, contact_form=contact_form, contact_info=contact_info, google_maps=google_maps, social_media_login=social_media_login, user_dashboard=user_dashboard, invoice_history=invoice_history, profile_settings=profile_settings, subscription_model=subscription_model, live_chat_support=live_chat_support, search_function=search_function, tip_feature=tip_feature, rating_system=rating_system, blog_posts=blog_posts)
    return result # returns string   

with st.form(key='website_generator'):
    #Get header image from the user
    uploaded_file = st.file_uploader("Upload Header Image", type=["png", "jpg", "jpeg"], key='header_image')
    if uploaded_file is not None:
        # Create a temporary file to store the uploaded content
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            header_image = temp_file.name # it shows the file path
    else:
        header_image = ''
    #Get call-to-action text from the user
    cta_text = st.text_input("Enter call-to-action text")
    #Get concept introduction from the user
    concept_intro = st.text_area("Enter concept introduction")
    #Get mission statement from the user
    mission_statement = st.text_area("Enter your mission statement")
    #Get service overview from the user
    service_overview = st.text_area("Enter service overview")
    #Get customer reviews from the user
    customer_reviews = st.text_area("Enter customer reviews")
    #Get footer links from the user
    footer_links = st.text_input("Enter footer links")
    #Get language selection from the user
    language_selection = st.selectbox("Select the language", ["English", "Spanish", "French", "German", "Italian"])
    #Get login/register option from the user
    login_register = st.selectbox("Select an option", ["Login", "Register"])
    #Get detailed service description from the user
    detailed_service_description = st.text_area("Enter detailed service description")
    #Get online booking option from the user
    online_booking = st.selectbox("Do you want to book online?", ["Yes", "No"])
    #Get booking process guide from the user
    booking_process_guide = st.text_area("Enter booking process guide")
    #Get FAQ from the user
    faq = st.text_area("Enter FAQ")
    #Get platform history from the user
    platform_history = st.text_area("Enter platform history")
    #Get team introduction from the user
    team_intro = st.text_area("Enter team introduction")
    #Get mission and vision from the user
    mission_vision = st.text_area("Enter your mission and vision")
    #Get contact form from the user
    contact_form = st.text_input("Enter contact form details")
    #Get contact information from the user
    contact_info = st.text_input("Enter your contact information")
    #Get Google Maps integration from the user
    google_maps = st.text_input("Enter Google Maps integration")
    #Get social media login option from the user
    social_media_login = st.selectbox("Select your social media login option", ["Facebook", "Twitter", "Google", "LinkedIn"])
    #Get user dashboard features from the user
    user_dashboard = st.multiselect("Select dashboard features", ["Analytics", "Reports", "Notifications", "Settings", "Profile"])
    #Get invoice history option from the user
    invoice_history = st.checkbox("Do you want to see invoice history?")
    #Get profile settings option from the user
    profile_settings = st.selectbox("Select profile settings", ["Public", "Private", "Friends Only"])
    #Get subscription model from the user
    subscription_model = st.selectbox("Select your subscription model", ["Monthly", "Yearly", "Lifetime"])
    #Get live chat support option from the user
    live_chat_support = st.checkbox("Do you want live chat support?")
    #Get search function from the user
    search_function = st.text_input("Enter search function")
    #Get tip feature from the user
    tip_feature = st.text_input("Enter tip feature")
    #Get rating system from the user
    rating_system = st.text_input("Enter the rating system")
    #Get blog posts from the user
    blog_posts = st.text_area("Enter your blog posts")
    submit_button = st.form_submit_button(label='Generate Website')
    if submit_button:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            website = ""
        elif header_image and cta_text and concept_intro and mission_statement and service_overview and customer_reviews and footer_links and language_selection and login_register and detailed_service_description and online_booking and booking_process_guide and faq and platform_history and team_intro and mission_vision and contact_form and contact_info and google_maps and social_media_login and user_dashboard and invoice_history and profile_settings and subscription_model and live_chat_support and search_function and tip_feature and rating_system and blog_posts:
            website = websiteGenerator(header_image,cta_text,concept_intro,mission_statement,service_overview,customer_reviews,footer_links,language_selection,login_register,detailed_service_description,online_booking,booking_process_guide,faq,platform_history,team_intro,mission_vision,contact_form,contact_info,google_maps,social_media_login,user_dashboard,invoice_history,profile_settings,subscription_model,live_chat_support,search_function,tip_feature,rating_system,blog_posts)
        else:
            website = ""
        #Display the generated website to the user
        if website:
            st.markdown(website, unsafe_allow_html=True)
