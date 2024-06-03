import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from data_set1.data_set1_dict import data1_dict
import pickle
from sklearn.decomposition import TruncatedSVD, PCA


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

range_n_clusters = [2, 3, 4, 5, 6,7,8]
elbow = []
ss = []
for n_clusters in range_n_clusters:
   #iterating through cluster sizes
   clusterer = KMeans(n_clusters = n_clusters, random_state=42)
   cluster_labels = clusterer.fit_predict(reduced_data)
   #Finding the average silhouette score
   silhouette_avg = silhouette_score(reduced_data, cluster_labels)
   ss.append(silhouette_avg)
   print("For n_clusters =", n_clusters,"The average silhouette_score is :", silhouette_avg)
   #Finding the average SSE"
   elbow.append(clusterer.inertia_) # Inertia: Sum of distances of samples to their closest cluster center
fig = plt.figure(figsize=(14,7))
fig.add_subplot(121)
plt.plot(range_n_clusters, elbow,'b-',label='Sum of squared error')
plt.xlabel("Number of cluster")
plt.ylabel("SSE")
plt.legend()
fig.add_subplot(122)
plt.plot(range_n_clusters, ss,'b-',label='Silhouette Score')
plt.xlabel("Number of cluster")
plt.ylabel("Silhouette Score")
plt.legend()
plt.show()