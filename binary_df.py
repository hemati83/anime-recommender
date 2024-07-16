import pandas as pd
import numpy as np

# import tsv to dataframe and remove brackets from genre lists
df = pd.read_csv("./animes.tsv", sep="\t")
df["genres"] = df["genres"].str.strip("[]")

# create zeros dataframe of all genres and cast values appropriately for training
all_genres = ["Action", "Adventure", "Avant Garde", "Award Winning", "Boys Love", "Comedy", "Drama", "Fantasy", "Girls Love", "Gourmet", "Horror", "Mystery", "Romance", "Sci-Fi", "Slice of Life", "Sports", "Supernatural", "Suspense", "Ecchi", "Erotica", "Hentai", "Adult Cast", "Anthropomorphic", "CGDCT", "Childcare", "Combat Sports", "Crossdressing", "Delinquents", "Detective", "Educational", "Gag Humor", "Gore", "Harem", "High Stakes Game", "Historical", "Idols (Female)", "Idols (Male)", "Isekai", "Iyashikei", "Love Polygon", "Magical Sex Shift", "Mahou Shoujo", "Martial Arts", "Mecha", "Medical", "Military", "Music", "Mythology", "Organized Crime", "Otaku Culture", "Parody", "Performing Arts", "Pets", "Psychological", "Racing", "Reincarnation", "Reverse Harem", "Romantic Subtext", "Samurai", "School", "Showbiz", "Space", "Strategy Game", "Super Power", "Survival", "Team Sports", "Time Travel", "Vampire", "Video Game", "Visual Arts", "Workplace", "Josei", "Kids", "Seinen", "Shoujo", "Shounen"]
all_genres = sorted(all_genres)
zeros = pd.DataFrame(0, index=np.arange(len(df)), columns=all_genres)
zeros = zeros.astype(int)

# create binary matrix for genres
for i in range(len(df)):
    # strip strings and convert to lists of genres per anime
    genre_string = df.iloc[i]["genres"]
    genre_string = genre_string.replace("'", "").replace(",", "")
    genre_list = genre_string.split()

    # assign 1 in appropriate column in zeros dataframe
    for item in genre_list:
        zeros.iloc[i][item] = 1

# write training data to tsv
zeros.to_csv(path_or_buf="./training_data.tsv", sep="\t")