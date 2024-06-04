from sklearn.metrics.pairwise import cosine_similarity 
import pandas as pd
import numpy as np
import pickle
from nltk.tokenize import word_tokenize
from data_set1.query_dict import query_dict
from data_set1.qrel_mini import qrel_list_mini
from data_set1.qrel_list import qrel_list
from data_set1.data_set1_dict import data1_dict

from data_set2.qrel2_mini import qrel2_list_mini
from data_set2.qrel2_list import qrel2_list
from data_set2.query2_dict import query2_dict
from data_set2.data_set2_dict import data2_dict
from text_processing import TextProcessor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import average_precision_score
 

def calc_MAP(dataset_number) :
    
    y_true=[]# Binary relevance labels (1 if relevant, 0 if not)
    y_scores=[]# Scores or binary predictions from the retrieval system
    AP=[]
    myqrel_list=[]
    myqrel_list=[]
    dataset={}
   
    if dataset_number==1:
         myquery_list=query_dict
         myqrel_list=qrel_list_mini
         dataset=data1_dict
         with open('vectorizer_obj.pkl', 'rb') as file: 
            print("vectorizer_obj loaded")
            vectorizer_obj = pickle.load(file) 
         with open('tfidf_matrix.pkl', 'rb') as file: 
            print("tfidf_matrix loaded")
            tfidf_matrix = pickle.load(file)    
    elif dataset_number==2:
         myquery_list=query2_dict
         myqrel_list=qrel2_list_mini
         dataset=data2_dict
         with open('vectorizer_obj2.pkl', 'rb') as file: 
            #print("vectorizer_obj loaded")
            vectorizer_obj = pickle.load(file) 
         with open('tfidf_matrix2.pkl', 'rb') as file: 
            #print("tfidf_matrix loaded")
            tfidf_matrix = pickle.load(file)    

    for key,value in myquery_list.items():
        query_vector = vectorizer_obj.transform([value])
        similarity_matrix = cosine_similarity(query_vector,tfidf_matrix)
        similarity_threshold=0.02
        doc_ids = dataset.keys()
        document_ranking = dict(zip(doc_ids, similarity_matrix.flatten()))
        filtered_documents = {key: value for key, value in document_ranking.items() if value >= similarity_threshold}
        sorted_dict = sorted(filtered_documents.items(), key=lambda item: item[1], reverse=True)
        query_retrived_list=[]
        query_precision_list=[]
        real_relevant=myqrel_list.get(key)
        for i in range(10):
            if sorted_dict[i][0] in real_relevant:
               query_retrived_list.append(1)
               query_precision_list.append(len(query_retrived_list)/(i+1))
               #print(f"len(query_retrived_list):{len(query_retrived_list)} ,index {i+1}")
                       
                   
       
        y_true.append(query_retrived_list)          
        y_scores.append(query_precision_list)
        if len(query_retrived_list) != 0 :
           AP.append(sum(query_precision_list)/len(query_retrived_list))
           #print(f"relevant : {len(query_retrived_list)}")
    #print(f"Mean Average Precision (MAP): {round((sum(AP)/len(myquery_list))*100,2)} %")
    return round((sum(AP)/len(myquery_list))*100)
          

def calc_MRR(dataset_number):
    reciprocal_rank=[]# Scores or binary predictions from the retrieval system
    if dataset_number==1:
         myquery_list=query_dict
         myqrel_list=qrel_list_mini
         dataset=data1_dict
         with open('vectorizer_obj.pkl', 'rb') as file: 
            print("vectorizer_obj loaded")
            vectorizer_obj = pickle.load(file) 
         with open('tfidf_matrix.pkl', 'rb') as file: 
            print("tfidf_matrix loaded")
            tfidf_matrix = pickle.load(file)    
    elif dataset_number==2:
         myquery_list=query2_dict
         myqrel_list=qrel2_list_mini
         dataset=data2_dict
         with open('vectorizer_obj2.pkl', 'rb') as file: 
            print("vectorizer_obj2 loaded")
            vectorizer_obj = pickle.load(file) 
         with open('tfidf_matrix2.pkl', 'rb') as file: 
            print("tfidf_matrix2 loaded")
            tfidf_matrix = pickle.load(file)    
    for key,value in myquery_list.items():
    
        query_vector = vectorizer_obj.transform([value])
        similarity_matrix = cosine_similarity(query_vector,tfidf_matrix)
        similarity_threshold=0.02
        doc_ids = dataset.keys()
        document_ranking = dict(zip(doc_ids, similarity_matrix.flatten()))
        filtered_documents = {key: value for key, value in document_ranking.items() if value >= similarity_threshold}
        sorted_dict = sorted(filtered_documents.items(), key=lambda item: item[1], reverse=True)
        real_relevant=myqrel_list.get(key)
        for i in range(10):
            if sorted_dict[i][0] in real_relevant:
               reciprocal_rank.append(1/(i+1))
               continue
                       
        # for qrel in myqrel_list:
        #     if key == qrel.query_id: 
        #         for i in range(10):
        #             if sorted_dict[i][0] == qrel.doc_id and qrel.relevance != 0:
        #                 reciprocal_rank.append(1/(i+1)) # 1/rank
        #                 continue
                   
       
    print(f"Mean Reciprocal Rank (MRR): {round((sum(reciprocal_rank)/len(query2_dict))*100)}%")
    return round((sum(reciprocal_rank)/len(myquery_list))*100)
          

def calc_precision(query,id,dataset_number):
    relvant=0
    if dataset_number==1:
         myqrel_list=qrel_list
         dataset=data1_dict
         with open('vectorizer_obj.pkl', 'rb') as file: 
            print("vectorizer_obj loaded")
            vectorizer_obj = pickle.load(file) 
         with open('tfidf_matrix.pkl', 'rb') as file: 
            print("tfidf_matrix loaded")
            tfidf_matrix = pickle.load(file)    
    elif dataset_number==2:
         myqrel_list=qrel2_list
         dataset=data2_dict
         with open('vectorizer_obj2.pkl', 'rb') as file: 
            print("vectorizer_obj2 loaded")
            vectorizer_obj = pickle.load(file) 
         with open('tfidf_matrix2.pkl', 'rb') as file: 
            print("tfidf_matrix2 loaded")
            tfidf_matrix = pickle.load(file)
    query_vector = vectorizer_obj.transform([query])
    similarity_matrix = cosine_similarity(query_vector,tfidf_matrix)
    similarity_threshold=0.02
    doc_ids = dataset.keys()
    document_ranking = dict(zip(doc_ids, similarity_matrix.flatten()))
    filtered_documents = {key: value for key, value in document_ranking.items() if value >= similarity_threshold}
    sorted_dict = sorted(filtered_documents.items(), key=lambda item: item[1], reverse=True)
    for qrel in myqrel_list:
       
        if id == qrel.query_id and qrel.relevance != 0: 
          for i in range(10):
             if sorted_dict[i][0] == qrel.doc_id:
                relvant+=1
    
    print(f"precision @K {id} = {relvant/10}") 
    return relvant/10



def calc_Recall(query,id,dataset_number):
    relvant=0
    total_relvent=0
    if dataset_number==1:
         myqrel_list=qrel_list
         dataset=data1_dict
         total_relvent=len(qrel_list_mini.get(id))
         with open('vectorizer_obj.pkl', 'rb') as file: 
            print("vectorizer_obj loaded")
            vectorizer_obj = pickle.load(file) 
         with open('tfidf_matrix.pkl', 'rb') as file: 
            print("tfidf_matrix loaded")
            tfidf_matrix = pickle.load(file)    
    elif dataset_number==2:
         myqrel_list=qrel2_list
         dataset=data2_dict
         total_relvent=len(qrel2_list_mini.get(id))
         with open('vectorizer_obj2.pkl', 'rb') as file: 
            print("vectorizer_obj2 loaded")
            vectorizer_obj = pickle.load(file) 
         with open('tfidf_matrix2.pkl', 'rb') as file: 
            print("tfidf_matrix2 loaded")
            tfidf_matrix = pickle.load(file)
    query_vector = vectorizer_obj.transform([query])
    similarity_matrix = cosine_similarity(query_vector,tfidf_matrix)
    similarity_threshold=0.02
    doc_ids = dataset.keys()
    document_ranking = dict(zip(doc_ids, similarity_matrix.flatten()))
    filtered_documents = {key: value for key, value in document_ranking.items() if value >= similarity_threshold}
    sorted_dict = sorted(filtered_documents.items(), key=lambda item: item[1], reverse=True)
    for qrel in myqrel_list:
        if id == qrel.query_id and qrel.relevance != 0: 
           for i in range(10):
              if sorted_dict[i][0] == qrel.doc_id:
                 relvant+=1
    
    # print(f"relvant {id} = {relvant} , total_relvent :{total_relvent} ")  
    print(f"Recall {id} = {relvant/total_relvent}")  

    return round(relvant/total_relvent,2)


def calc_avg_recall(dataset_number):
     total=0
     avg=0
     myquery={}
     if dataset_number==1:
         myquery=query_dict
     elif dataset_number==2:
         myquery=query2_dict    
     for key,value in myquery.items():
        total+=1
        avg+=calc_Recall(query=value,id=key,dataset_number=dataset_number)
     return round(avg/total,2)

def calc_avg_precision(dataset_number):
     total=0
     avg=0
     myquery={}
     if dataset_number==1:
         myquery=query_dict
     elif dataset_number==2:
         myquery=query2_dict    
     for key,value in myquery.items():
        total+=1
        avg+=calc_precision(query=value,id=key,dataset_number=dataset_number)
     return round(avg/total,2)


