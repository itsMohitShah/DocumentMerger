print("Loading LinkedInMessager module ...")
import os
import pyperclip
import logging
from Utils.Logging import logger  # Import the logger from your Logging module

def main_copymessage(path_LinkedInMessage, list_names):
    """
    Reads a LinkedIn message template from a file and replaces placeholders with the provided name.
    
    Args:
        path_LinkedInMessage (str): Path to the LinkedIn message template file.
        list_names (list): Names to replace in the template.
    """
    try:
        logger.info(f"Reading LinkedIn message template from: {path_LinkedInMessage}")
        
        # Read the message template
        with open(path_LinkedInMessage, 'r', encoding='utf-8') as file:
            message_template = file.read()
        logger.info("Read the LinkedIn message template.")
        name = list_names[0]
        # Replace the placeholder with the provided name
        message = message_template.replace("{name}", name)
        logger.info(f"Replaced placeholder with name: {name}")
        
        # Copy the message to clipboard
        pyperclip.copy(message)
        logger.info("LinkedIn message copied to clipboard successfully.")
        
        print(f"LinkedIn message copied to clipboard:\n{message}")
    except FileNotFoundError:
        logger.error(f"LinkedIn message template file not found: {path_LinkedInMessage}")
    except Exception as e:
        logger.error(f"Error reading LinkedIn message template: {e}")