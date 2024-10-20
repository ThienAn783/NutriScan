# utils.py

def format_number(value):
    if value is not None:
        formatted = f"{value:.10f}"
        return f"{formatted.rstrip('0').rstrip('.')}"
    else:
        return '0'
