import pandas as pd
import pickle
from data_set1.data_set1_dict import data1_dict
from data_set2.data_set2_dict import data2_dict
from text_processing import TextProcessor
from sklearn.feature_extraction.text import TfidfVectorizer

def indexing_dataset(dataset_number):
    if dataset_number==1:
        dataset=data1_dict
    elif dataset_number==2:
        dataset=data2_dict    
# Create an instance of TextProcessor
 

    processor = TextProcessor()

    documents = list(dataset.values())

    vectorizer = TfidfVectorizer(preprocessor=processor.process_text)

    tfidf_matrix = vectorizer.fit_transform(documents)

    if dataset_number==1:

        with open('vectorizer_obj.pkl', 'wb') as file: 
            
            pickle.dump(vectorizer, file) 

        with open('tfidf_matrix.pkl', 'wb') as file: 
            
            pickle.dump(tfidf_matrix, file) 
    elif dataset_number==2:  
         with open('vectorizer_obj2.pkl', 'wb') as file: 
            
            pickle.dump(vectorizer, file) 

         with open('tfidf_matrix2.pkl', 'wb') as file: 
            
            pickle.dump(tfidf_matrix, file)       


def indexing_data(dict):
# Create an instance of TextProcessor
    processor = TextProcessor(dict)

    documents = list(dict.values())

    vectorizer = TfidfVectorizer(preprocessor=processor.process_text)

    tfidf_matrix = vectorizer.fit_transform(documents)

    with open('vectorizer_obj2.pkl', 'wb') as file: 
        
        pickle.dump(vectorizer, file) 

    with open('tfidf_matrix2.pkl', 'wb') as file: 
        
        pickle.dump(tfidf_matrix, file) 

    df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out(), index=dict.keys())
    
    return df

