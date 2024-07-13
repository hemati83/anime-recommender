import requests
import time
import json
import pandas as pd

# access token
access_token = json.load(open("./token.json"))["access_token"]

# helper function: requires limit, offset, and the auth token and returns anime ids as a list in the order of their current rank
def ranked_ids(limit, offset, access_token):
    url = "https://api.myanimelist.net/v2/anime/ranking"
    params = {
            "ranking_type": "tv",
            "limit": limit,
            "offset": offset,
    }
    headers = {
            "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(url, params = params, headers = headers)
    if response.status_code == 200:
        anime_data = response.json()
        anime_ids = [entry["node"]["id"] for entry in anime_data["data"][:]]
        return anime_ids
    else:
        print(f"Failed to retrieve top anime. Status code: {response.status_code}")
        return []
    
# helper function: requires anime_ids, fields, and access_token and returns anime details
def ranked_details(anime_id, fields, access_token):
    url = f"https://api.myanimelist.net/v2/anime/{anime_id}"
    params = {
            "fields": fields,
    }
    headers = {
            "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(url, params = params, headers = headers)
    if response.status_code == 200:
        anime_details = response.json()
        return anime_details
    else:
        print(f"Failed to retrieve information. Status code: {response.status_code}")

# helper writer function to write to a file
# def writer(path, array):
#     with open(path, "w") as file:
#         for item in array:
#             file.write(str(item) + "\n")

# requires token and returns nothing
# writes anime ids to file
def anime_ids(limit, init_offset):
    # cast inputs
    limit = int(limit)
    init_offset = int(init_offset)
    print("Using token to grab anime ids...\n")

    # api max is 500
    api_max = 500

    # list to append to
    global anime_id_list
    anime_id_list = []

    # loop over floor + 1 times
    for i in range((limit // api_max) + 1):
        offset = init_offset + api_max * i
        anime_id_list += ranked_ids(min(limit, api_max), offset, access_token)
        limit = max(0, limit - api_max)

# requires token and returns nothing
# writes relevant anime details to respective files
def anime_details():
    fields = "title, mean, rank, popularity, genres"
    fields_list = ["title", "mean", "rank", "popularity", "genres"]
    print("Using token to grab anime details...\n")

    # now we have ids, so we can loop over each to get info
    anime_dict = {field: [] for field in fields_list}

    for i, anime_id in enumerate(anime_id_list):
        anime_details = ranked_details(anime_id, fields, access_token)
        for field in fields_list:
            if field == "genres":
                genre_list = []
                for element in anime_details[field]:
                    genre_list.append(element['name'])
                anime_dict[field].append(genre_list)
            else:
                anime_dict[field].append(anime_details[field])
        if i % 100 == 0:
            print("Finished with anime rank #" + str(i))
            print("Just give it a bit to write the relevant data :^)")
            time.sleep(60) # arbitrary number to bypass api call frequency

    # use pandas to format the data into a dataframe and write to tsv
    df = pd.DataFrame.from_dict(anime_dict)
    df.to_csv(path_or_buf="./data.tsv", sep="\t")

if __name__ == '__main__':
    piss = input("Input amount of anime to grab: ")
    piss2 = input("Input offset from rank #1: ")
    ids = anime_ids(piss, piss2)
    anime_details()