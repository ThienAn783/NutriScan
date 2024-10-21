# utils.py

def format_number(value):
    """
    Formats a number to remove unnecessary trailing zeros and decimal points.

    Parameters:
    - value: The numerical value to format.

    Returns:
    - A string representation of the formatted number.
    """
    if value is not None:
        try:
            formatted = f"{float(value):.10f}".rstrip('0').rstrip('.')
            return formatted if formatted else '0'
        except (ValueError, TypeError):
            return '0'
    else:
        return '0'
