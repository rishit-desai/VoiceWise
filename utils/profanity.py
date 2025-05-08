import re
import string
import json
# Use a pipeline as a high-level helper
from transformers import pipeline
import streamlit as st
import os
import torch

torch.classes.__path__ = []  # streamlit issue with torch classes


def get_profanity_list():
    return json.load(open(os.path.dirname(__file__)+'\\profanity_list.json', 'r')) # reference: https://github.com/zacanger/profane-words/blob/master/words.json

def profanity_filter_regex(text):
    """
    Check if the text contains any profanity using regex.
    Args:
        text (str): The text to check for profanity.
    Returns:
        bool: True if profanity is found, False otherwise.
    """

    # Load the profanity list from a JSON file
    profanity_list = get_profanity_list() 
    # Create a regex pattern to match any word in the profanity list
    pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in profanity_list) + r')\b', re.IGNORECASE)

    was_found = pattern.search(text)
    if was_found:
        return True
    else:
        return False

def regex_implementation(conversation_array):
    """
    Check if the conversation contains any profanity using regex.
    Args:
        conversation_array (list): The list of conversation dictionaries.
    Returns:
        tuple: A tuple containing two boolean values indicating if profanity was found in the customer and agent texts.
    """

    all_agent_text = "".join([conv["text"] for conv in conversation_array if conv["speaker"] == "Agent"])
    all_customer_text = "".join([conv["text"] for conv in conversation_array if conv["speaker"] == "Customer"])

    customer_profanity = profanity_filter_regex(all_customer_text)
    agent_profanity = profanity_filter_regex(all_agent_text)

    return customer_profanity, agent_profanity


@st.cache_resource
def get_pipeline():
    # Load the pipeline for text classification
    return pipeline("text-classification", model="Zohair101/Foul-Language-Detection-DH") # reference: https://huggingface.co/Zohair101/Foul-Language-Detection-DH/tree/main


def profanity_detector_ml(text):
    # Use the pipeline to classify the text
    pipe = get_pipeline()
    result = pipe(text)[0]

    if result['label'] == 'LABEL_0':
        return True
    else:
        return False


def ml_implementation(conversation_array):
    """
    Check if the conversation contains any profanity using a machine learning model.
    Args:
        conversation_array (list): The list of conversation dictionaries.
    Returns:
        tuple: A tuple containing two boolean values indicating if profanity was found in the customer and agent texts.
    """
    

    customer_profanity = False
    agent_profanity = False

    all_agent_text = "".join([conv["text"] for conv in conversation_array if conv["speaker"] == "Agent"])
    all_customer_text = "".join([conv["text"] for conv in conversation_array if conv["speaker"] == "Customer"])

    if len(conversation_array) != 0:
        if profanity_detector_ml(all_agent_text):
            agent_profanity = True
        if profanity_detector_ml(all_customer_text):
            customer_profanity = True
    return customer_profanity, agent_profanity
