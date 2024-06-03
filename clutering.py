import pickle
import pandas as pd
import re
import os
import numpy as np
import gensim
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from gensim.models import Doc2Vec
import matplotlib.pyplot as plt
from data_set2.data_set2_dict import data2_dict
from data_set1.data_set1_dict import data1_dict

from sklearn.feature_extraction.text import TfidfVectorizer

from text_processing import TextProcessor


train= data1_dict
LabeledSentence1 = gensim.models.doc2vec.TaggedDocument
all_content_train = []
j = 0

for key, text in train.items():
    all_content_train.append(LabeledSentence1(text, [key]))
    j += 1

print("Number of texts processed: ", j)

# d2v_model = Doc2Vec(all_content_train,window = 10,vector_size=100,min_count = 500, workers=7, dm = 1,alpha=0.025, min_alpha=0.001)
# d2v_model.train(all_content_train, total_examples=d2v_model.corpus_count, epochs=10, start_alpha=0.002, end_alpha=-0.016)   
# d2v_model.save("doc2vec_model")
# with open('d2v_model.pkl', 'wb') as file:  
#             pickle.dump(d2v_model, file) 

# d2v_model=Doc2Vec.load('doc2vec_model')
# # Convert text data to numerical vectors using TF-IDF
# processor=TextProcessor()
# vectorizer = TfidfVectorizer(max_features=10000,preprocessor=processor.process_text)
# data = vectorizer.fit_transform(data1_dict.values())
# # Apply PCA to reduce dimensions for visualization
# pca = PCA(n_components=2)
# datapoint = pca.fit_transform(data)

# # Plot the original data before clustering
# plt.figure(figsize=(12, 6))

# plt.subplot(1, 2, 1)
# plt.scatter(datapoint[:, 0], datapoint[:, 1], c='gray')
# plt.title('Original Data')
# plt.xlabel('PCA Component 1')
# plt.ylabel('PCA Component 2')

# # Perform KMeans clustering
# kmeans_model = KMeans(n_clusters=4, init='k-means++', max_iter=100)
# labels = kmeans_model.fit_predict(data)

# # Get the colors for each cluster label
# label_colors = ['#FFFF00', '#008000', '#0000FF', '#800080']
# color = [label_colors[i] for i in labels]

# # Plot the clustered data with labels
# plt.subplot(1, 2, 2)
# plt.scatter(datapoint[:, 0], datapoint[:, 1], c=color)
# plt.title('Clustered Data')
# plt.xlabel('PCA Component 1')
# plt.ylabel('PCA Component 2')

# # Plot the centroids
# centroids = kmeans_model.cluster_centers_
# centroidpoint = pca.transform(centroids)
# plt.scatter(centroidpoint[:, 0], centroidpoint[:, 1], marker='^', s=150, c='#000000')

# plt.show()


# # kmeans_model = KMeans(n_clusters=4, init='k-means++', max_iter=100) 
# # X = kmeans_model.fit(d2v_model.docvecs.doctag_syn0)
# # labels=kmeans_model.labels_.tolist()
# # l = kmeans_model.fit_predict(d2v_model.docvecs.doctag_syn0)
# # pca = PCA(n_components=2).fit(d2v_model.docvecs.doctag_syn0)
# # datapoint = pca.transform(d2v_model.docvecs.doctag_syn0)
# # plt.figure
# # label1 = ['#FFFF00', '#008000', '#0000FF', '#800080']
# # color = [label1[i] for i in labels]
# # plt.scatter(datapoint[:, 0], datapoint[:, 1], c=color)
# # centroids = kmeans_model.cluster_centers_
# # centroidpoint = pca.transform(centroids)
# # plt.scatter(centroidpoint[:, 0], centroidpoint[:, 1], marker='^', s=150, c='#000000')
# # plt.show()

# #model = Doc2Vec.load("doc2vec_model") 

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD, PCA
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer

# Example data dictionary
data_dict =data1_dict
# Convert text data to numerical vectors using TF-IDF
with open('vectorizer_obj.pkl', 'rb') as file: 
             vectorizer = pickle.load(file) 
#vectorizer = TfidfVectorizer(max_features=10000)  # Limit the number of features
data = vectorizer.fit_transform(data_dict.values())

# Apply Truncated SVD to reduce dimensions while keeping the data sparse
svd = TruncatedSVD(n_components=100)  # Reduce to 100 dimensions
reduced_data = svd.fit_transform(data)

# Apply PCA to further reduce dimensions for visualization
pca = PCA(n_components=2)
datapoint = pca.fit_transform(reduced_data)

# Plot the original data before clustering
plt.figure(figsize=(12, 6))

# plt.subplot(1, 2, 1)
# plt.scatter(datapoint[:, 0], datapoint[:, 1], c='gray')
# plt.title('Original Data')
# plt.xlabel('PCA Component 1')
# plt.ylabel('PCA Component 2')

# Perform MiniBatchKMeans clustering
kmeans_model = MiniBatchKMeans(n_clusters=3, init='k-means++', max_iter=100)
with open('kmeans_model.pkl', 'wb') as file: 
            pickle.dump(kmeans_model, file) 

labels = kmeans_model.fit_predict(reduced_data)

# Get the colors for each cluster label , '#800080'
label_colors = ['#FFFF00', '#008000', '#0000FF']
color = [label_colors[i] for i in labels]

# Plot the clustered data with labels
plt.subplot(1, 2, 2)
plt.scatter(datapoint[:, 0], datapoint[:, 1], c=color)
plt.title('Clustered Data')
# plt.xlabel('PCA Component 1')
# plt.ylabel('PCA Component 2')

# Plot the centroids
centroids = kmeans_model.cluster_centers_
centroidpoint = pca.transform(centroids)
plt.scatter(centroidpoint[:, 0], centroidpoint[:, 1], marker='^', s=150, c='#000000')

plt.show()
