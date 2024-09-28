import sys

braille_dict = {
    'a': 'O.....', 
    'b': 'O.O...', 
    'c': 'OO....', 
    'd': 'OO.O..', 
    'e': 'O..O..',
    'f': 'OOO...', 
    'g': 'OOOO..', 
    'h': 'O.OO..', 
    'i': '.OO...', 
    'j': '.OOO..',
    'k': 'O...O.', 
    'l': 'O.O.O.', 
    'm': 'OO..O.', 
    'n': 'OO.OO.', 
    'o': 'O..OO.',
    'p': 'OOO.O.', 
    'q': 'OOOOO.', 
    'r': 'O.OOO.', 
    's': '.OO.O.', 
    't': '.OOOO.',
    'u': 'O...OO', 
    'v': 'O.O.OO', 
    'w': '.OOO.O', 
    'x': 'OO..OO', 
    'y': 'OO.OOO',
    'z': 'O..OOO', 
    ' ': '......',
    '0': '.OOO..', 
    '1': 'O.....', 
    '2': 'O.O...', 
    '3': 'OO....', 
    '4': 'OO.O..',
    '5': 'O..O..', 
    '6': 'OOO...', 
    '7': 'OOOO..', 
    '8': 'O.OO..', 
    '9': '.OO...',
    'capital_follows': '.....O',    
    'decimal_follows': '.O...O',    
    'number_follows': '....OO',     
    '.': '..OO.O',                  
    ',': '..O...',                  
    '?': '..O.OO',                  
    '!': '..OOO.',                  
    ':': '..OO..',                  
    ';': '..O.O.',                  
    '-': '....OO',                  
    '/': '.O..O.',                  
    '<': '.OO..O',                  
    '>': 'O..OO.',                  
    '(': 'O.O..O',                  
    ')': '.O.OO.',                  
}

# Create English to Braille mapping (letters, numbers, punctuation, space)
english_to_braille = {}
for key, value in braille_dict.items():
    if key.isalnum() or key in [' ', '.', ',', '?', '!', ':', ';', '-', '/', '<', '>', '(', ')']:
        english_to_braille[key] = value
braille_to_english = {v: k for k, v in braille_dict.items()}

# Define special indicators
CAPITAL_INDICATOR = braille_dict['capital_follows']  # '.....O'
NUMBER_INDICATOR = braille_dict['number_follows']    # '....OO'
DECIMAL_INDICATOR = braille_dict['decimal_follows']  # '.O...O'

# Function to determine if input is Braille
def is_braille(s):
    allowed_chars = set(['O', '.'])
    return all(c in allowed_chars for c in s) and len(s) % 6 == 0

# Function to translate English to Braille
def english_to_braille_translate(text):
    braille = []
    in_number = False

    for char in text:
        if char.isupper():
            # Capital letter: prepend capital indicator
            braille.append(CAPITAL_INDICATOR)
            braille.append(english_to_braille.get(char.lower(), '......'))
            in_number = False  # Exit number mode if active
        elif char.isdigit():
            if not in_number:
                # Start number mode: prepend number indicator
                braille.append(NUMBER_INDICATOR)
                in_number = True
            braille.append(english_to_braille.get(char, '......'))
        elif char == ' ':
            braille.append(english_to_braille[' '])
            in_number = False  # Exit number mode
        elif char in english_to_braille:
            braille.append(english_to_braille[char.lower()])
            in_number = False  # Exit number mode
        else:
            # Handle punctuation if present
            braille.append(english_to_braille.get(char, '......'))
            in_number = False  # Exit number mode

    return ''.join(braille)

# Function to translate Braille to English
def braille_to_english_translate(braille_str):
    english = []
    cells = [braille_str[i:i+6] for i in range(0, len(braille_str), 6)]
    i = 0
    in_number = False
    capitalize_next = False

    while i < len(cells):
        cell = cells[i]

        if cell == CAPITAL_INDICATOR:
            capitalize_next = True
            i += 1
            continue
        elif cell == NUMBER_INDICATOR:
            in_number = True
            i += 1
            continue
        elif cell == DECIMAL_INDICATOR:
            english.append('.')
            in_number = False
            i += 1
            continue
        elif cell == braille_dict[' ']:
            english.append(' ')
            in_number = False
            i += 1
            continue

        if in_number:
            if cell in braille_to_english:
                english_char = braille_to_english[cell]
                if english_char.isdigit():
                    english.append(english_char)
                else:
                    # If not a digit, exit number mode and process normally
                    in_number = False
                    if english_char.isalpha():
                        if capitalize_next:
                            english.append(english_char.upper())
                            capitalize_next = False
                        else:
                            english.append(english_char)
                    else:
                        english.append(english_char)
            else:
                # Unknown cell in number mode
                english.append('?')
            i += 1
        else:
            if cell in braille_to_english:
                english_char = braille_to_english[cell]
                if english_char.isalpha():
                    if capitalize_next:
                        english.append(english_char.upper())
                        capitalize_next = False
                    else:
                        english.append(english_char)
                elif english_char.isdigit():
                    # Digit without number indicator; handle as is
                    english.append(english_char)
                else:
                    # Punctuation or other symbols
                    english.append(english_char)
            else:
                # Unknown cell
                english.append('?')
            i += 1

    return ''.join(english)

def main():
    if len(sys.argv) < 2:
        print("Usage: python translator.py <text>")
        sys.exit(1)
    
    input_text = ''.join(sys.argv[1:])  # Remove spaces between arguments for Braille input
    
    if is_braille(input_text):
        translated = braille_to_english_translate(input_text)
    else:
        translated = english_to_braille_translate(input_text)
    
    print(translated)

if __name__ == "__main__":
    main()
