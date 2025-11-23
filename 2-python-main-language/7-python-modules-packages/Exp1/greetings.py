# greetings.py

def say_hello(name):
    """Return a personalized greeting."""
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
