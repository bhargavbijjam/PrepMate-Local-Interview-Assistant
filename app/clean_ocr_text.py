import re
from spellchecker import SpellChecker

spell = SpellChecker()

def clean_text(text):
    # Fix common OCR errors
    text = text.replace('\n', ' ')              # remove newlines
    text = re.sub(r'[^a-zA-Z0-9\s,.]', '', text) # remove junk chars
    text = re.sub(r'\s+', ' ', text)            # normalize spaces

    # Spell correction (simple word-by-word)
    corrected_words = []
    for word in text.split():
        if word.lower() not in spell:
            corrected = spell.correction(word)
            corrected_words.append(corrected if corrected else word)
        else:
            corrected_words.append(word)
    
    return ' '.join(corrected_words)
