from sklearn.cluster import KMeans
import pandas as pd

# import dataframes
animes = pd.read_csv("./animes.tsv", sep="\t")
training_data = pd.read_csv("./training_data.tsv", sep="\t")

# designate training data & initialize K-means clustering
X = training_data
kmeans = KMeans(n_clusters=50, random_state=83)
kmeans.fit(X)

# get data cluster label for each anime
cluster_labels = kmeans.labels_

# get input and acquire respective data cluster label
watched = input("Input the title of the anime you enjoyed exactly as it appears on MyAnimeList (CASE-SENSITIVE): ")
watched_index = animes[animes["title"] == watched].index.values
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