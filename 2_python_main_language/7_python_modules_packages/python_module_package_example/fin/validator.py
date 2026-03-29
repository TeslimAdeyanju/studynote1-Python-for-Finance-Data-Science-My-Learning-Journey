# validators.py

def is_valid_amount(amount):
    """Check if an amount is a valid positive number"""
    try:
        return float(amount) > 0
    except (ValueError, TypeError):
        return False


def is_valid_date_range(start_date, end_date):
    """Check if start date is before end date"""
    return start_date < end_date