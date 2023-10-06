# All library imports

import os
import shutil
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

# Get openai_api_key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

### Copy and paste all the functions as is

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to log in to the Guidewire Policy Center application with the specified role
def login_to_policy_center(role):
    # Log in to the Guidewire Policy Center application with the specified role
    if role == "Agent":
        st.session_state.messages.append(SystemMessagePromptTemplate("Agent logged in"))
    elif role == "Underwriter":
        st.session_state.messages.append(SystemMessagePromptTemplate("Underwriter logged in"))
    else:
        st.session_state.messages.append(SystemMessagePromptTemplate("Invalid role"))

# Invoke the function
login_to_policy_center(role)

#Create a new policy by entering all required and mandatory information
def create_new_policy(information):
    # Check if the user is logged in as an Underwriter
    if role != "Underwriter":
        st.session_state.messages.append(SystemMessagePromptTemplate("Only Underwriters can create new policies"))
        return
    
    # Validate the information provided
    if not information:
        st.session_state.messages.append(SystemMessagePromptTemplate("Please provide all required information"))
        return
    
    # Create a new policy using the provided information
    st.session_state.messages.append(SystemMessagePromptTemplate("Creating a new policy..."))
    time.sleep(2)  # Simulating policy creation process
    
    # Display the created policy details
    st.session_state.messages.append(SystemMessagePromptTemplate("New policy created successfully"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Policy Number: ABC123"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Policy Holder: John Doe"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Effective Date: 2022-01-01"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Premium Amount: $1000"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Coverage: Auto Insurance"))
    
# Invoke the function
create_new_policy(information)

# Validate the underwriting rules to ensure accurate policy issuance
def validate_underwriting_rules():
    # Check if the user is logged in as an Underwriter
    if role != "Underwriter":
        st.session_state.messages.append(SystemMessagePromptTemplate("Only Underwriters can validate underwriting rules"))
        return
    
    # Get the policy details from the session state
    policy_number = "ABC123"
    policy_holder = "John Doe"
    effective_date = "2022-01-01"
    premium_amount = "$1000"
    coverage = "Auto Insurance"
    
    # Display the policy details
    st.session_state.messages.append(SystemMessagePromptTemplate("Policy Details:"))
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Policy Number: {policy_number}"))
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Policy Holder: {policy_holder}"))
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Effective Date: {effective_date}"))
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Premium Amount: {premium_amount}"))
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Coverage: {coverage}"))
    
    # Validate the underwriting rules
    st.session_state.messages.append(SystemMessagePromptTemplate("Validating underwriting rules..."))
    time.sleep(2)  # Simulating underwriting rules validation process
    
    # Display the validation result
    st.session_state.messages.append(SystemMessagePromptTemplate("Underwriting rules validated successfully"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Policy is eligible for issuance"))
    
# Invoke the function
validate_underwriting_rules()

# Rate the quote and issue the policy
def rate_and_issue_policy(quote):
    # Check if the user is logged in as an Underwriter
    if role != "Underwriter":
        st.session_state.messages.append(SystemMessagePromptTemplate("Only Underwriters can rate and issue policies"))
        return
    
    # Check if a quote is provided
    if not quote:
        st.session_state.messages.append(SystemMessagePromptTemplate("Please provide a quote"))
        return
    
    # Display the quote details
    st.session_state.messages.append(SystemMessagePromptTemplate("Quote Details:"))
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Quote Number: {quote['quote_number']}"))
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Quote Amount: {quote['quote_amount']}"))
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Coverage: {quote['coverage']}"))
    
    # Rate the quote
    st.session_state.messages.append(SystemMessagePromptTemplate("Rating the quote..."))
    time.sleep(2)  # Simulating quote rating process
    
    # Display the rating result
    st.session_state.messages.append(SystemMessagePromptTemplate("Quote rated successfully"))
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Premium Amount: {quote['premium_amount']}"))
    
    # Issue the policy
    st.session_state.messages.append(SystemMessagePromptTemplate("Issuing the policy..."))
    time.sleep(2)  # Simulating policy issuance process
    
    # Display the policy issuance result
    st.session_state.messages.append(SystemMessagePromptTemplate("Policy issued successfully"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Policy is active"))
    
# Invoke the function
quote = {
    "quote_number": "Q123",
    "quote_amount": "$1200",
    "coverage": "Auto Insurance",
    "premium_amount": "$1000"
}
rate_and_issue_policy(quote)

# Verify that all information displayed on the policy after issuance matches the entered details
def verify_policy_information():
    # Check if the user is logged in as an Underwriter
    if role != "Underwriter":
        st.session_state.messages.append(SystemMessagePromptTemplate("Only Underwriters can verify policy information"))
        return
    
    # Get the entered policy details
    entered_policy_number = "ABC123"
    entered_policy_holder = "John Doe"
    entered_effective_date = "2022-01-01"
    entered_premium_amount = "$1000"
    entered_coverage = "Auto Insurance"
    
    # Get the displayed policy details
    displayed_policy_number = "ABC123"
    displayed_policy_holder = "John Doe"
    displayed_effective_date = "2022-01-01"
    displayed_premium_amount = "$1000"
    displayed_coverage = "Auto Insurance"
    
    # Compare the entered details with the displayed details
    if (entered_policy_number == displayed_policy_number and
        entered_policy_holder == displayed_policy_holder and
        entered_effective_date == displayed_effective_date and
        entered_premium_amount == displayed_premium_amount and
        entered_coverage == displayed_coverage):
        st.session_state.messages.append(SystemMessagePromptTemplate("Policy information verified successfully"))
    else:
        st.session_state.messages.append(SystemMessagePromptTemplate("Policy information does not match the entered details"))

# Invoke the function
verify_policy_information()

# Log in to the Guidewire Policy Center application with the specified role
def login_to_policy_center(role):
    # Log in to the Guidewire Policy Center application with the specified role
    if role == "Agent":
        st.session_state.messages.append(SystemMessagePromptTemplate("Agent logged in"))
    elif role == "Underwriter":
        st.session_state.messages.append(SystemMessagePromptTemplate("Underwriter logged in"))
    else:
        st.session_state.messages.append(SystemMessagePromptTemplate("Invalid role"))

# Invoke the function
login_to_policy_center(role)

# Search for existing policies based on relevant search criteria
def search_existing_policies(search_criteria):
    # Check if the user is logged in as an Underwriter
    if role != "Underwriter":
        st.session_state.messages.append(SystemMessagePromptTemplate("Only Underwriters can search for existing policies"))
        return
    
    # Check if search criteria is provided
    if not search_criteria:
        st.session_state.messages.append(SystemMessagePromptTemplate("Please provide search criteria"))
        return
    
    # Perform the search based on the search criteria
    st.session_state.messages.append(SystemMessagePromptTemplate("Searching for existing policies..."))
    time.sleep(2)  # Simulating search process
    
    # Display the search results
    policies = [
        {
            "policy_number": "ABC123",
            "policy_holder": "John Doe",
            "effective_date": "2022-01-01",
            "premium_amount": "$1000",
            "coverage": "Auto Insurance"
        },
        {
            "policy_number": "DEF456",
            "policy_holder": "Jane Smith",
            "effective_date": "2022-02-01",
            "premium_amount": "$1200",
            "coverage": "Home Insurance"
        }
    ]
    
    st.session_state.messages.append(SystemMessagePromptTemplate("Search Results:"))
    for policy in policies:
        st.session_state.messages.append(SystemMessagePromptTemplate(f"Policy Number: {policy['policy_number']}"))
        st.session_state.messages.append(SystemMessagePromptTemplate(f"Policy Holder: {policy['policy_holder']}"))
        st.session_state.messages.append(SystemMessagePromptTemplate(f"Effective Date: {policy['effective_date']}"))
        st.session_state.messages.append(SystemMessagePromptTemplate(f"Premium Amount: {policy['premium_amount']}"))
        st.session_state.messages.append(SystemMessagePromptTemplate(f"Coverage: {policy['coverage']}"))

# Invoke the function
search_criteria = {
    "policy_holder": "John Doe",
    "coverage": "Auto Insurance"
}
search_existing_policies(search_criteria)

# Retrieve the selected existing policy
def retrieve_existing_policy():
    # Check if the user is logged in as an Underwriter
    if role != "Underwriter":
        st.session_state.messages.append(SystemMessagePromptTemplate("Only Underwriters can retrieve existing policies"))
        return
    
    # Get the policy number of the selected policy
    selected_policy_number = "ABC123"
    
    # Retrieve the selected policy from the database
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Retrieving policy {selected_policy_number}..."))
    time.sleep(2)  # Simulating retrieval process
    
    # Display the retrieved policy details
    st.session_state.messages.append(SystemMessagePromptTemplate("Policy Details:"))
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Policy Number: {selected_policy_number}"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Policy Holder: John Doe"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Effective Date: 2022-01-01"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Premium Amount: $1000"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Coverage: Auto Insurance"))

# Invoke the function
retrieve_existing_policy()

# Initiate post transactions on the policy
def initiate_post_transactions():
    # Check if the user is logged in as an Underwriter
    if role != "Underwriter":
        st.session_state.messages.append(SystemMessagePromptTemplate("Only Underwriters can initiate post transactions"))
        return
    
    # Get the policy number of the selected policy
    selected_policy_number = "ABC123"
    
    # Display the selected policy details
    st.session_state.messages.append(SystemMessagePromptTemplate("Selected Policy Details:"))
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Policy Number: {selected_policy_number}"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Policy Holder: John Doe"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Effective Date: 2022-01-01"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Premium Amount: $1000"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Coverage: Auto Insurance"))
    
    # Perform the post transactions on the policy
    st.session_state.messages.append(SystemMessagePromptTemplate("Initiating post transactions..."))
    time.sleep(2)  # Simulating post transaction process
    
    # Display the result of the post transactions
    st.session_state.messages.append(SystemMessagePromptTemplate("Post transactions initiated successfully"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Policy updated"))
    st.session_state.messages.append(SystemMessagePromptTemplate("New effective date: 2022-02-01"))
    st.session_state.messages.append(SystemMessagePromptTemplate("New premium amount: $1100"))

# Invoke the function
initiate_post_transactions()

# Update the policy information as required
def update_policy_information(policy_information):
    # Check if the user is logged in as an Underwriter
    if role != "Underwriter":
        st.session_state.messages.append(SystemMessagePromptTemplate("Only Underwriters can update policy information"))
        return
    
    # Check if policy information is provided
    if not policy_information:
        st.session_state.messages.append(SystemMessagePromptTemplate("Please provide policy information"))
        return
    
    # Get the policy number of the selected policy
    selected_policy_number = "ABC123"
    
    # Display the selected policy details
    st.session_state.messages.append(SystemMessagePromptTemplate("Selected Policy Details:"))
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Policy Number: {selected_policy_number}"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Policy Holder: John Doe"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Effective Date: 2022-01-01"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Premium Amount: $1000"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Coverage: Auto Insurance"))
    
    # Update the policy information
    st.session_state.messages.append(SystemMessagePromptTemplate("Updating policy information..."))
    time.sleep(2)  # Simulating policy information update process
    
    # Display the updated policy information
    st.session_state.messages.append(SystemMessagePromptTemplate("Policy information updated successfully"))
    st.session_state.messages.append(SystemMessagePromptTemplate("New effective date: 2022-02-01"))
    st.session_state.messages.append(SystemMessagePromptTemplate("New premium amount: $1100"))

# Invoke the function
policy_information = {
    "effective_date": "2022-02-01",
    "premium_amount": "$1100"
}
update_policy_information(policy_information)

# Quote and issue the policy for the updated information
def quote_and_issue_policy():
    # Check if the user is logged in as an Underwriter
    if role != "Underwriter":
        st.session_state.messages.append(SystemMessagePromptTemplate("Only Underwriters can quote and issue policies"))
        return
    
    # Check if the updated policy information is provided
    if not policy_information:
        st.session_state.messages.append(SystemMessagePromptTemplate("Please provide updated policy information"))
        return
    
    # Get the policy number of the selected policy
    selected_policy_number = "ABC123"
    
    # Display the selected policy details
    st.session_state.messages.append(SystemMessagePromptTemplate("Selected Policy Details:"))
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Policy Number: {selected_policy_number}"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Policy Holder: John Doe"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Effective Date: 2022-01-01"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Premium Amount: $1000"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Coverage: Auto Insurance"))
    
    # Quote the updated policy
    st.session_state.messages.append(SystemMessagePromptTemplate("Quoting the updated policy..."))
    time.sleep(2)  # Simulating quote process
    
    # Display the quote details
    st.session_state.messages.append(SystemMessagePromptTemplate("Quote Details:"))
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Quote Number: Q123"))
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Quote Amount: $1200"))
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Coverage: Auto Insurance"))
    
    # Issue the policy
    st.session_state.messages.append(SystemMessagePromptTemplate("Issuing the policy..."))
    time.sleep(2)  # Simulating policy issuance process
    
    # Display the policy issuance result
    st.session_state.messages.append(SystemMessagePromptTemplate("Policy issued successfully"))
    st.session_state.messages.append(SystemMessagePromptTemplate("Policy is active"))

# Invoke the function
quote_and_issue_policy()

# Verify that all information displayed on the policy after issuance reflects the updated details
def verify_updated_policy_information():
    # Check if the user is logged in as an Underwriter
    if role != "Underwriter":
        st.session_state.messages.append(SystemMessagePromptTemplate("Only Underwriters can verify policy information"))
        return
    
    # Get the updated policy details
    updated_policy_number = "ABC123"
    updated_policy_holder = "John Doe"
    updated_effective_date = "2022-02-01"
    updated_premium_amount = "$1100"
    updated_coverage = "Auto Insurance"
    
    # Get the displayed policy details
    displayed_policy_number = "ABC123"
    displayed_policy_holder = "John Doe"
    displayed_effective_date = "2022-02-01"
    displayed_premium_amount = "$1100"
    displayed_coverage = "Auto Insurance"
    
    # Compare the updated details with the displayed details
    if (updated_policy_number == displayed_policy_number and
        updated_policy_holder == displayed_policy_holder and
        updated_effective_date == displayed_effective_date and
        updated_premium_amount == displayed_premium_amount and
        updated_coverage == displayed_coverage):
        st.session_state.messages.append(SystemMessagePromptTemplate("Policy information verified successfully"))
    else:
        st.session_state.messages.append(SystemMessagePromptTemplate("Policy information does not reflect the updated details"))

# Invoke the function
verify_updated_policy_information()

# Log in to the Guidewire Policy Center application with the specified role
def login_to_policy_center(role):
    # Log in to the Guidewire Policy Center application with the specified role
    if role == "Agent":
        st.session_state.messages.append(SystemMessagePromptTemplate("Agent logged in"))
    elif role == "Underwriter":
        st.session_state.messages.append(SystemMessagePromptTemplate("Underwriter logged in"))
    else:
        st.session_state.messages.append(SystemMessagePromptTemplate("Invalid role"))

# Invoke the function
login_to_policy_center(role)

# Review underwriting referrals
def review_underwriting_referrals():
    # Check if the user is logged in as an Underwriter
    if role != "Underwriter":
        st.session_state.messages.append(SystemMessagePromptTemplate("Only Underwriters can review underwriting referrals"))
        return
    
    # Retrieve the assigned referrals from the database
    assigned_referrals = [
        {
            "referral_number": "R123",
            "policy_number": "ABC123",
            "policy_holder": "John Doe",
            "referral_reason": "High risk driver",
            "assigned_to": "Underwriter A"
        },
        {
            "referral_number": "R456",
            "policy_number": "DEF456",
            "policy_holder": "Jane Smith",
            "referral_reason": "Unusual property",
            "assigned_to": "Underwriter B"
        }
    ]
    
    # Display the assigned referrals
    st.session_state.messages.append(SystemMessagePromptTemplate("Assigned Referrals:"))
    for referral in assigned_referrals:
        st.session_state.messages.append(SystemMessagePromptTemplate(f"Referral Number: {referral['referral_number']}"))
        st.session_state.messages.append(SystemMessagePromptTemplate(f"Policy Number: {referral['policy_number']}"))
        st.session_state.messages.append(SystemMessagePromptTemplate(f"Policy Holder: {referral['policy_holder']}"))
        st.session_state.messages.append(SystemMessagePromptTemplate(f"Referral Reason: {referral['referral_reason']}"))
        st.session_state.messages.append(SystemMessagePromptTemplate(f"Assigned To: {referral['assigned_to']}"))

# Invoke the function
review_underwriting_referrals()

# Function to approve the referrals as reviewed, indicating their assessment
def approve_referrals():
    # Check if the user is logged in as an Underwriter
    if role != "Underwriter":
        st.session_state.messages.append(SystemMessagePromptTemplate("Only Underwriters can approve referrals"))
        return
    
    # Get the referral numbers of the referrals to be approved
    referral_numbers = ["R123", "R456"]
    
    # Approve the referrals as reviewed
    st.session_state.messages.append(SystemMessagePromptTemplate("Approving referrals as reviewed..."))
    time.sleep(2)  # Simulating approval process
    
    # Display the result of the approval
    st.session_state.messages.append(SystemMessagePromptTemplate("Referrals approved as reviewed"))
    for referral_number in referral_numbers:
        st.session_state.messages.append(SystemMessagePromptTemplate(f"Referral {referral_number} reviewed and approved"))

# Invoke the function
approve_referrals()

# Verify Policy Status
def verify_policy_status():
    # Check if the user is logged in as an Underwriter
    if role != "Underwriter":
        st.session_state.messages.append(SystemMessagePromptTemplate("Only Underwriters can verify policy status"))
        return
    
    # Get the policy number of the selected policy
    selected_policy_number = "ABC123"
    
    # Retrieve the policy status from the database
    policy_status = "Active"
    
    # Display the policy status
    st.session_state.messages.append(SystemMessagePromptTemplate(f"Policy Status: {policy_status}"))

# Invoke the function
verify_policy_status()

### Create a form

with st.form(key='story_game'):
    # Under the form, take all the user inputs
    role = st.radio("Select your role", ["Agent", "Underwriter"])
    information = st.text_input(label='Enter policy information')
    search_criteria = st.text_input(label='Enter search criteria')
    text_input = st.text_input(label='Enter some text')
    submit_button = st.form_submit_button(label='Submit Story')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        # Invoke the functions based on user inputs
        login_to_policy_center(role)
        create_new_policy(information)
        validate_underwriting_rules()
        rate_and_issue_policy(quote)
        verify_policy_information()
        login_to_policy_center(role)
        search_existing_policies(search_criteria)
        retrieve_existing_policy()
        initiate_post_transactions()
        update_policy_information(policy_information)
        quote_and_issue_policy()
        verify_updated_policy_information()
        login_to_policy_center(role)
        review_underwriting_referrals()
        approve_referrals()
        verify_policy_status()
        #Under the st.form_submit_button, show the results.
        for message in st.session_state.messages:
            st.write(message)

#############################################################