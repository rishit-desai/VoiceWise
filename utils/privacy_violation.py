import streamlit as st
from transformers import pipeline
import re
import torch

torch.classes.__path__ = []  # streamlit issue with torch classes

@st.cache_resource
def get_pipeline():
    # Use a pipeline as a high-level helper

    return pipeline("text-classification", model="barek2k2/bert_hipaa_sensitive_db_schema") # reference: https://huggingface.co/barek2k2/bert_hipaa_sensitive_db_schema/tree/main

def sensitive_information_detector_ml(text):
    """
    Check if the text contains sensitive information using a pre-trained model.
    Args:
        text (str): The text to check for sensitive information.
    Returns:
        bool: True if sensitive information is found, False otherwise.
    """

    # Use the pipeline to classify the text
    pipe = get_pipeline()
    result = pipe(text)[0]

    if result['label'] == 'LABEL_0':
        return False
    else:
        return True

def privacy_and_compliance_violation_ml_implementation(conversation_array):
    """
    Check if the conversation contains any privacy and compliance violations using a pre-trained model.
    Args:
        conversation_array (list): The list of conversation dictionaries.
    Returns:
        tuple: A tuple containing two boolean values indicating if privacy and compliance violations were found in the customer and agent texts.
    """
    customer_privacy = False
    agent_privacy_revealed_info = False

    all_agent_text = "".join(
        [conv["text"] for conv in conversation_array if conv["speaker"] == "Agent"]
    )

    # check if agent text contains dollar value (bank balance)
    if check_money_value(all_agent_text):
        agent_privacy_revealed_info = True

    if agent_privacy_revealed_info:
        all_customer_text = "".join([conv["text"] for conv in conversation_array if conv["speaker"] == "Customer"])

        if sensitive_information_detector_ml(all_customer_text):
            customer_privacy = True


    return customer_privacy, True if agent_privacy_revealed_info and not customer_privacy else False

def check_money_value(text):
    # Check if the text contains a dollar value (bank balance) followed by a number of any length

    pattern = r'\$\d+(\.\d{2})?'
    match = re.search(pattern, text)
    if match:
        return True
    else:
        return False


def sensitive_information_detector_regex(text):
    ssn_number = r'\b\d{3}-\d{2}-\d{4}\b'  # SSN format: XXX-XX-XXXX
    phone_number = r'\b\d{3}-\d{3}-\d{4}\b'  # Phone number format: XXX-XXX-XXXX
    email_address = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'  # Email address format
    credit_card = r'\b\d{4}-\d{4}-\d{4}-\d{4}\b'  # Credit card format: XXXX-XXXX-XXXX-XXXX
    address = r'\d+\s\w+\s\w+,\s\w+'  # Address format: 123 Main St, City
    date = r'\b\w+\s\d{1,2},\s\d{4}\b'  # Date format: Month DD, YYYY    

    # Create a regex pattern to match any of the sensitive information formats
    pattern = re.compile(r'(' + '|'.join([ssn_number, phone_number, email_address, credit_card, address, date]) + r')')

    was_found = pattern.search(text)
    if was_found:
        return True
    else:
        return False


def privacy_and_compliance_violation_regex_implementation(conversation_array):
    """
    Check if the conversation contains any privacy and compliance violations using regex.
    Args:
        conversation_array (list): The list of conversation dictionaries.
    Returns:
        tuple: A tuple containing two boolean values indicating if privacy and compliance violations were found in the customer and agent texts.
    """
    customer_privacy = False
    agent_privacy_revealed_info = False

    all_agent_text = "".join(
        [conv["text"] for conv in conversation_array if conv["speaker"] == "Agent"]
    )

    # check if agent text contains dollar value (bank balance)
    if check_money_value(all_agent_text):
        agent_privacy_revealed_info = True

    if agent_privacy_revealed_info:
        all_customer_text = "".join([conv["text"] for conv in conversation_array if conv["speaker"] == "Customer"])

        if sensitive_information_detector_regex(all_customer_text):
            customer_privacy = True


    return customer_privacy, True if agent_privacy_revealed_info and not customer_privacy else False
