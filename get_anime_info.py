import requests
import time
import json


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
def writer(path, array, append_status):
    if append_status:
        write_type = "a"

    else:
        write_type = "w"

    with open(path, write_type) as file:
        for item in array:
            file.write(str(item) + "\n")


# helper function: returns text
def get_text(path):
    with open(path, "r") as file:
        raw_text = file.read().strip()

    return raw_text


# requires token and returns nothing
# writes anime ids to file
def anime_ids(limit, init_offset, append_status):

    # correct types for the function
    limit = int(limit)
    init_offset = int(init_offset)
    append_status = bool(append_status)

    # app info
    path_access_token = "./token.json"
    f = open(path_access_token)
    access_token = json.load(f)["access_token"]

    print("Using token...\n")

    # api max is 500
    api_max = 500

    # empty list to join to
    anime_ids = []

    # loop over floor + 1 times
    for i in range((limit // api_max) + 1):
        offset = init_offset + api_max * i

        anime_ids += ranked_ids(min(limit, api_max), offset, access_token)
        limit = max(0, limit - api_max)

    path_ids = "./anime-info/anime_ids.txt"
    writer(path_ids, anime_ids, append_status)


# requires token and returns nothing
# writes anime details to respective files
def anime_details(append_status):
    fields = input("Available fields: id, title, main_picture, alternative_titles, start_date, end_date, synopsis, mean, rank, popularity, num_list_users, num_scoring_users, nsfw, genres, created_at, updated_at, media_type, status, my_list_status, num_episodes, start_season, broadcast, source, average_episode_duration, rating, studios, pictures, background, related_anime, related_manga, recommendations, statistics, videos. \n Please type wanted fields separated by commas: ")
    fields_list = fields.split(", ")

    # ask user for type of picture if they want pictures
    if "main_picture" in fields_list:
        size_type = input("I noticed you wanted 'main_picture'. Do you want 'medium' or 'large'?: ")

    # correct types for the function
    append_status = bool(append_status)

    # app info
    path_access_token = "./token.json"
    f = open(path_access_token)
    access_token = json.load(f)["access_token"]

    print("Using token...\n")

    # paths
    path_anime_ids = "./anime-info/anime_ids.txt"
    path_list = ["./anime-info/" + field + ".txt" for field in fields_list]

    # api max is 500
    api_max = 500

    # now we have ids, so we can loop over each to get info
    anime_dict = {field: [] for field in fields_list}

    with open(path_anime_ids, "r") as file:
        anime_ids = file.read().splitlines()

    for i, anime_id in enumerate(anime_ids):
        anime_details = ranked_details(anime_id, fields, access_token)

        for field in fields_list:

            if field == "main_picture":
                anime_dict[field].append(anime_details[field][size_type])

            elif field == "videos":
                if anime_details[field] ==  []:
                    anime_dict[field].append("None")

                else:
                    anime_dict[field].append(anime_details[field][0]["url"])

            else:
                anime_dict[field].append(anime_details[field])

        if i % 100 == 0:
            print("Finished with anime rank #" + str(i))
            time.sleep(60) # arbitrary number to bypass api call frequency

    for i, field in enumerate(fields_list):
        writer(path_list[i], anime_dict[field], append_status)


if __name__ == '__main__':
    piss = input("limit")
    piss2 = input("init_offset")
    piss4 = input("append_status (boolean)")
    if piss4.lower() == "true":
        append = True
    else:
        append = False
    ids = anime_ids(piss, piss2, append)
    anime_details(append)