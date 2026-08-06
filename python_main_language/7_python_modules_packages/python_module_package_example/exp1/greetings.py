# greetings.py
"""
Greetings Module
================

This module provides functions for creating personalized greetings.

Functions:
    say_hello(name): Returns a hello message
    say_goodbye(name): Returns a goodbye message
    get_greeting_stats(): Returns module statistics

Author: Your Name
Version: 1.0.0
"""
def say_hello(name):
    """
    Generate a personalized hello message.

    Args:
        name (str): The person's name

    Returns:
        str: A formatted greeting message

    Example:
        >>> say_hello("Alice")
        'Hello, Alice! Welcome to Python modules!'
    """
    return f"Hello, {name}! Welcome to Python modules!"

def say_goodbye(name):
    """Return a personalized farewell."""
    return f"Goodbye, {name}! Thanks for using our module!"

def get_greeting_stats():
    """Return statistics about greetings."""
    return {
        'total_greetings': 2,
        'languages': ['English'],
        'author': 'Your Name'
    }

# Module-level variable
MODULE_VERSION = "1.0.0"
DEFAULT_GREETING = "Hello, World!"

# This runs when the module is imported
print(f"Greetings module v{MODULE_VERSION} loaded successfully!")
