import pickle
import pandas as pd
import gensim
from sklearn.cluster import KMeans
from gensim.models import Doc2Vec
import matplotlib.pyplot as plt
from data_set2.data_set2_dict import data2_dict
from data_set1.data_set1_dict import data1_dict
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD, PCA
from sklearn.cluster import MiniBatchKMeans
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


# Example data dictionary
data_dict =data2_dict
# Convert text data to numerical vectors using TF-IDF
with open('vectorizer_obj2.pkl', 'rb') as file: 
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
kmeans_model = MiniBatchKMeans(n_clusters=2, init='k-means++', max_iter=100)
with open('kmeans_model.pkl', 'wb') as file: 
            pickle.dump(kmeans_model, file) 

labels = kmeans_model.fit_predict(reduced_data)

# Get the colors for each cluster label , '#800080'
label_colors = ['#FFFF00', '#008000']
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
