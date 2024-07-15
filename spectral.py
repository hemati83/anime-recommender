from sklearn.cluster import SpectralClustering
import pandas as pd

# import dataframes
animes = pd.read_csv("./animes.tsv", sep="\t")
training_data = pd.read_csv("./training_data.tsv", sep="\t")

# designate training data & initialize Spectral Clustering
X = training_data
spectral = SpectralClustering(n_clusters=50)

# get cluster label for each anime
cluster_labels = spectral.fit_predict(X)

# get input and acquire respective data cluster label
user_in = input("Input the title of the anime you enjoyed exactly as it appears on MyAnimeList (CASE-SENSITIVE)\nIf necessary, copy and paste the title from animes.tsv: ")
watched_index = animes[animes["title"] == user_in].index.values
target_cluster = cluster_labels[watched_index[0]]

# get animes that are in the same cluster
matches = []
for idx, cluster in enumerate(cluster_labels):
    if cluster == target_cluster:
        if idx == watched_index: continue
        else: matches.append(idx)

# display the titles of the top 10 related anime series by rank with desired offset
offset = int(input("Enter your desired offset (note that higher offsets may lead to lower ranked suggestions): "))
suggestions = []
counter = 0
for idx in matches[offset:]:
    if counter == 10: break
    counter += 1
    suggestions.append(animes["title"][idx])
print(suggestions)