import re

"""
Extracts all floating-point numbers from the given text.

Args:
    text (str): The text to extract floating-point numbers from.

Returns:
    list: A list of floating-point numbers found in the text.
"""
def extract_floats(text):

    result = re.findall(r"(?<!\d)[-+]?\d*\.?\d+(?!\d)", text)

    if len(result) == 0:
        return ["---"]

    return result


"""
Cleans the table header by replacing specific strings with their corresponding replacements.

Args:
    header (str): The header string to be cleaned.

Returns:
    str: The cleaned header string.
"""
def clean_header(header):
    replacements = {
        # Alice
        'AC': 'AC', 'AO': 'AO', 'AM': 'AM',
        'Soma Ap': 'Soma', 'HIP': 'HIP',
        'Eventos A + H': 'Eventos A',
        'RERA': 'RERA', 'Eventos resp': 'Eventos\nresp.',

        'REM nº/h (REM)': 'REM nº/h (REM)', 'NREM nº/h (NREM)' : 'NREM nº/h (NREM)',
        'TTS nº/h (sono)': 'TTS nº/h (sono)',

        'Duração total (min)': 'Duração total',

        'A + H -> IAH (nº/h)': 'IAH',

        #short report

        
    }
    for key, value in replacements.items():
        if value in header:
            return key
    return header

def safe_float(value):
    try:
        return float(value.replace(",", ".").strip())
    except (ValueError, TypeError):
        return 0.0