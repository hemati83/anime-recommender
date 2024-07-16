import pandas as pd
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.mixture import GaussianMixture
from sklearn.cluster import SpectralClustering

# requires model and returns array of cluster labels
# initialize model & grab array of cluster labels for each anime using training_data
def cluster(model):
    # K-Means
    if model == 1:
        kmeans = KMeans(n_clusters=61, random_state=83)
        cluster_labels = kmeans.fit_predict(training_data)
        return(cluster_labels)

    # Mini Batch K-Means
    elif model == 2:
        minibatch = MiniBatchKMeans(n_clusters=76, random_state=413)
        cluster_labels = minibatch.fit_predict(training_data)
        return(cluster_labels)

    # Gaussian Mixture Model
    elif model == 3:
        gaussian = GaussianMixture(n_components=55, random_state=100)
        cluster_labels = gaussian.fit_predict(training_data)
        return(cluster_labels)

    # Spectral Clustering
    elif model ==4:
        spectral = SpectralClustering(n_clusters=20, random_state=727)
        cluster_labels = spectral.fit_predict(training_data)
        return(cluster_labels)

    # handle invalid input
    else: 
        print("Invalid input.")
        exit()


# requires array of cluster labels and returns nothing
def print_suggestions(cluster_labels):
    # get user input
    user_in = input("Input the title of the anime you enjoyed exactly as it appears on MyAnimeList (CASE-SENSITIVE).\nIf necessary, copy and paste the title from animes.tsv: ")
    
    # handle invalid input
    if user_in not in animes["title"].tolist(): 
        print("Invalid input.")
        exit()

    # get the cluster label for the user input
    watched_index = animes[animes["title"] == user_in].index.values
    target_cluster = cluster_labels[watched_index[0]]

    # get animes that are in the same cluster
    matches = []
    for idx, cluster in enumerate(cluster_labels):
        if cluster == target_cluster:
            if idx == watched_index: continue
            else: matches.append(idx)

    # display the titles of the top 10 related anime series by rank with desired offset
    offset = int(input("Enter your desired offset (note that higher offsets lead to lower ranked suggestions): "))
    suggestions = []
    counter = 0
    for idx in matches[offset:]:
        if counter == 10: break
        counter += 1
        suggestions.append(animes["title"][idx])
    for series in suggestions:
        print(series)

if __name__ == "__main__":
    # import dataframes
    animes = pd.read_csv("./animes.tsv", sep="\t")
    training_data = pd.read_csv("./training_data.tsv", sep="\t")

    # initialize model based on user input
    model = int(input("Choose which type of model you want a recommendation from.\nType 1 for K-Means, 2 for Mini Batch K-Means, 3 for Gaussian Mixture Model, 4 for Spectral Clustering (this one takes a while): "))
    cluster_labels = cluster(model)

    # display recommendations
    print_suggestions(cluster_labels)