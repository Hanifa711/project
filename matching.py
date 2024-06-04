from itertools import islice
import pickle
import nltk
from nltk.corpus import stopwords
# from query_processing import QueryProcessor
from data_set1.data_set1_dict import data1_dict
from data_set2.data_set2_dict import data2_dict
from sklearn.metrics.pairwise import cosine_similarity 
import numpy as np

def match_collect_data(query,dataset_number):
    data_dict={}

    if dataset_number==1:
        data_dict=data1_dict
        with open('vectorizer_obj.pkl', 'rb') as file: 
             vectorizer_obj = pickle.load(file) 
        with open('tfidf_matrix.pkl', 'rb') as file: 
            tfidf_matrix = pickle.load(file)  

    elif dataset_number==2:
        data_dict=data2_dict
        with open('vectorizer_obj2.pkl', 'rb') as file: 
             vectorizer_obj = pickle.load(file) 
        with open('tfidf_matrix2.pkl', 'rb') as file: 
            tfidf_matrix = pickle.load(file)  
    
       
    query_vector = vectorizer_obj.transform([query])
    similarity_matrix = cosine_similarity(query_vector,tfidf_matrix)
    similarity_threshold=0.02
    doc_ids = data_dict.keys()
    document_ranking = dict(zip(doc_ids, similarity_matrix.flatten()))
    filtered_documents = {key: value for key, value in document_ranking.items() if value >= similarity_threshold}
    sorted_dict = sorted(filtered_documents.items(), key=lambda item: item[1], reverse=True)
    # print(sorted_dict[0])
    # Extract keys from sorted_dict
    keys_from_sorted_dict = {key for key, _ in sorted_dict}

    # Create a new dictionary by matching keys
    result_dict = {key: data_dict[key] for key in keys_from_sorted_dict if key in data_dict}
    # Get the first 10 items (if there are that many)
    first_10_items = dict(islice(result_dict.items(), 10))
    # print(first_10_items.keys())
    return first_10_items 


def match_data(query,dataset_number):
    data_dict={}

    if dataset_number==1:
        data_dict=data1_dict
        with open('vectorizer_obj.pkl', 'rb') as file: 
             vectorizer_obj = pickle.load(file) 
        with open('tfidf_matrix.pkl', 'rb') as file: 
            tfidf_matrix = pickle.load(file)  

    elif dataset_number==2:
        data_dict=data2_dict
        with open('vectorizer_obj2.pkl', 'rb') as file: 
             vectorizer_obj = pickle.load(file) 
        with open('tfidf_matrix2.pkl', 'rb') as file: 
            tfidf_matrix = pickle.load(file)  
    
       
    query_vector = vectorizer_obj.transform([query])
    similarity_matrix = cosine_similarity(query_vector,tfidf_matrix)
    similarity_threshold=0.02
    doc_ids = data_dict.keys()
    document_ranking = dict(zip(doc_ids, similarity_matrix.flatten()))
    filtered_documents = {key: value for key, value in document_ranking.items() if value >= similarity_threshold}
    sorted_dict = sorted(filtered_documents.items(), key=lambda item: item[1], reverse=True)
    return sorted_dict