import pickle
from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.cluster import MiniBatchKMeans
from data_set2.data_set2_dict import data2_dict
from data_set2.qrel2_mini import qrel2_list_mini
from data_set2.qrel2_list import qrel2_list
from data_set2.query2_dict import query2_dict

with open('vectorizer_obj2.pkl', 'rb') as file: 
             vectorizer = pickle.load(file) 
with open('tfidf_matrix2.pkl', 'rb') as file: 
             tfidf_matrix = pickle.load(file)
with open('kmeans_model2.pkl', 'rb') as file: 
             kmeans = pickle.load(file)  
             kmeans=kmeans.fit(tfidf_matrix)   

def find_relevant_documents(query,query_id,vectorizer=vectorizer, kmeans=kmeans, tfidf_matrix=tfidf_matrix, data_dict=data2_dict,similarity_threshold=0.2):
        # Step 1: Transform the query using the vectorizer
        query_vector = vectorizer.transform([query])
        
        # Step 2: Predict the cluster for the query using the k-means model
        query_cluster = kmeans.predict(query_vector)[0]
        # print("query_cluster : ",query_cluster)
        # Step 3: Filter documents belonging to the same cluster
        cluster_indices = [i for i, label in enumerate(kmeans.labels_) if label == query_cluster]

        # Map indices to document IDs
        doc_ids = list(data_dict.keys())
        index_to_doc_id = {i: doc_ids[i] for i in cluster_indices}    
        
        cluster_documents = {index_to_doc_id[idx]: data_dict[index_to_doc_id[idx]] for idx in cluster_indices}
        cluster_tfidf_matrix = tfidf_matrix[cluster_indices]
        # print("cluster_tfidf_matrix",cluster_tfidf_matrix)
        # Step 4: Calculate cosine similarity between the query and the documents in the cluster
        similarity_matrix = cosine_similarity(query_vector, cluster_tfidf_matrix)
        
        # Step 5: Filter and sort documents based on similarity threshold
        doc_ids = list(cluster_documents.keys())
        document_ranking = dict(zip(doc_ids, similarity_matrix.flatten()))
        filtered_documents = {key: value for key, value in document_ranking.items() if value >= similarity_threshold}
        sorted_documents = sorted(filtered_documents.items(), key=lambda item: item[1], reverse=True)        
        return sorted_documents    

 
# reacll_avg=0               
# for key,value in query2_dict.items():
#        reacll_avg+= find_relevant_documents(query=value,vectorizer= vectorizer,kmeans= kmeans,tfidf_matrix= tfidf_matrix,data_dict= data2_dict,query_id=key)
# print(f"reacll_avg {reacll_avg}")
# query = 'Vitamin D and COVID-19, Does Vitamin D impact COVID-19 prevention and treatment?, This includes studies describing possible role of Vitamin D in prevention of COVID-19, suppression of cytokine storm, clinical outcomes, and associations between Vitamin D status and COVID-19 mortality.'
# print(sorted_documents)


def calc_MAP_cluster() :
    
    y_true=[]# Binary relevance labels (1 if relevant, 0 if not)
    y_scores=[]# Scores or binary predictions from the retrieval system
    AP=[]
    myquery_list=query2_dict
    myqrel_list=qrel2_list_mini         

    for key,value in myquery_list.items():
 
        sorted_dict=find_relevant_documents(query=value,query_id=key)
        query_retrived_list=[]
        query_precision_list=[]
        real_relevant=myqrel_list.get(key)
        for i in range(len(sorted_dict)):
            if sorted_dict[i][0] in real_relevant:
               query_retrived_list.append(1)
               query_precision_list.append(len(query_retrived_list)/(i+1))
               #print(f"len(query_retrived_list):{len(query_retrived_list)} ,index {i+1}")
                       
            
        y_true.append(query_retrived_list)          
        y_scores.append(query_precision_list)
        if len(query_retrived_list) != 0 :
           AP.append(sum(query_precision_list)/len(query_retrived_list))
           #print(f"relevant : {len(query_retrived_list)}")
    print(f"Mean Average Precision (MAP): {round((sum(AP)/len(myquery_list))*100,2)} %")
    return round((sum(AP)/len(myquery_list))*100)
          

def calc_MRR_cluster():
    reciprocal_rank=[]# Scores or binary predictions from the retrieval system
    myquery_list=query2_dict
    myqrel_list=qrel2_list_mini
        
    for key,value in myquery_list.items():
       sorted_dict=find_relevant_documents(query=value,query_id=key)
       real_relevant=myqrel_list.get(key)
       for i in range(10):
            if sorted_dict[i][0] in real_relevant:
               reciprocal_rank.append(1/(i+1))
               continue
        
       
    print(f"Mean Reciprocal Rank (MRR): {round((sum(reciprocal_rank)/len(query2_dict))*100)}%")
    return round((sum(reciprocal_rank)/len(myquery_list))*100)
          

def calc_precision(query,id):
    relvant=0
    myqrel_list=qrel2_list    
    sorted_dict=find_relevant_documents(query=query,query_id=id)
    for qrel in myqrel_list:
        if id == qrel.query_id and qrel.relevance != 0: 
          for i in range(10):
             if sorted_dict[i][0] == qrel.doc_id:
                relvant+=1
    
    print(f"precision @K {id} = {relvant/10}") 
    return relvant/10



def calc_Recall(query,id):
    relvant=0
    myqrel_list=qrel2_list
    total_relvent=len(qrel2_list_mini.get(id))   
    sorted_dict=find_relevant_documents(query=query,query_id=id)
    for qrel in myqrel_list:
        if id == qrel.query_id and qrel.relevance != 0: 
           for i in range(10):
              if sorted_dict[i][0] == qrel.doc_id:
                 relvant+=1
    # print(f"cluster relvant for query : {id} = {relvant} , total_relvent :{total_relvent} ")  
    # print(f"Recall {id} = {round(relvant/total_relvent,2)}")  
    return (relvant/total_relvent)


def calc_avg_reacll_cluster():
     total=0
     avg=0
     for key,value in query2_dict.items():
        total+=1
        avg+=calc_Recall(query=value,id=key)
     return round(avg/total,2)

def calc_avg_precision_cluster():
     total=0
     avg=0 
     for key,value in query2_dict.items():
        total+=1
        avg+=calc_precision(query=value,id=key)
     return round(avg/total,2)
     
def check_correct_cluster(query,id):
        
        query_vector = vectorizer.transform([query]) 
               
        query_cluster = kmeans.predict(query_vector)[0]
        cluster_indices = [i for i, label in enumerate(kmeans.labels_) if label == query_cluster]

        doc_ids = list(data2_dict.keys())
        index_to_doc_id = {i: doc_ids[i] for i in cluster_indices}    
        
        cluster_documents = {index_to_doc_id[idx]: data2_dict[index_to_doc_id[idx]] for idx in cluster_indices}
        total_relvent=len(qrel2_list_mini.get(id))   
        real_relevant=qrel2_list_mini.get(id)
        relevant_count = 0
        for doc_id in cluster_documents.keys():
           if doc_id in real_relevant:
               relevant_count += 1
        #print(f"cluster relvant for query : {id} = {relevant_count} , total_relvent :{total_relvent} ")  
        #print(f"cluster relvant for query : {id} = {round((relevant_count/total_relvent),2)*100}")
        return (relevant_count/total_relvent)

# for key,value in query2_dict.items(): 
#    check_correct_cluster(id=key,query=value)        
def  calc_avg():
     avg = 0 
     for key,value in query2_dict.items(): 
           avg+=check_correct_cluster(id=key,query=value) 
     return round((avg/len(query2_dict)),2)*100     

