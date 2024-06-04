from typing import List
from spellchecker import SpellChecker
from nltk.corpus import words
from collections import Counter
from my_list import query_list
from my_list2 import query_list2

query_logs = query_list
query_logs2=query_list2



def suggest_corrected_query(text: str) -> str:
    spell = SpellChecker()
    word_set = set(words.words())

    # Split the text into tokens
    original_tokens = text.split()
    corrected_tokens = []

    # Spell check each token
    for token in original_tokens:
        if token in word_set:
            corrected_tokens.append(token)
        else:
            suggestions = spell.candidates(token)
            if suggestions:
                corrected_tokens.append(spell.correction(token))
            else:
                corrected_tokens.append(token)

    # Compare original and corrected tokens
    if original_tokens == corrected_tokens:
        return ""
    
    return ' '.join(corrected_tokens)


