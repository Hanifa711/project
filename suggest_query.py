from typing import List
from spellchecker import SpellChecker
from nltk.corpus import words
from collections import Counter
from my_list import query_list
from my_list2 import query_list2

query_logs = query_list
query_logs2=query_list2

def get_query_suggestions(query: str, dataset_number: int) -> list:
    global query_logs
    global query_logs2

    if dataset_number == 1:
        queries = query_logs
    else:
        queries = query_logs2

    suggestions = []
    query_terms = query.lower().split()
    query_freq = Counter(query_terms)

    for suggest_query in queries:
        suggest_query_terms = suggest_query.lower().split()
        if set(query_terms).intersection(set(suggest_query_terms)):
            freq = sum([query_freq[term] for term in set(query_terms) & set(suggest_query_terms)])
            suggestions.append((suggest_query, freq))

    return suggestions



def suggest_corrected_query(text: str):
    spell = SpellChecker()

    word_set = set(words.words())

    # Create a list to store the corrected tokens
    corrected_tokens = []

    # Spell check each token
    for token in text.split():
        if token in word_set:
            corrected_tokens.append(token)
        else:
            suggestions = spell.candidates(token)
            if suggestions:
                corrected_tokens.append(spell.correction(token))
            else:
                corrected_tokens.append(token)

    return ','.join(corrected_tokens)


def get_all_suggested_corrected(text):
    total=[]
    suggested=get_query_suggestions(dataset_number=1,query=text)
    corrected=suggest_corrected_query(text)
    total.extend(suggested)
    total.append(corrected)
    if len(total) >= 10:
        return total[:10]
    else:
        return total 

def correct_sentence_spelling(tokens: List[str]) -> List[str]:
    spell = SpellChecker()
    misspelled = spell.unknown(tokens)
    for i, token in enumerate(tokens):
        if token in misspelled:
            corrected = spell.correction(token)
            if corrected is not None:
                tokens[i] = corrected
    return tokens

# text = "This is a sampli sentinse withh speling erors."
# # words = word_tokenize(text)
# _suggest_corrected_query(text)      
# print(_suggest_corrected_query(text)  )
# # _get_query_suggestions("")
