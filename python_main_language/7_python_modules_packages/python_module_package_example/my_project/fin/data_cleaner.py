# data_cleaner.py

def remove_null_values(data_list):
    """Remove None or empty values from a list of financial data"""
    return [value for value in data_list if value is not None and value != '']


def format_currency(amount):
    """Format a number as currency with 2 decimal places"""
    return f"${amount:,.2f}"


def remove_duplicates(transactions):
    """Remove duplicate transactions from a list"""
    return list(set(transactions))