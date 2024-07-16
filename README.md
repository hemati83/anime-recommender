# anime-recommender

**Step 1:** Apply for a myanimelist client ID (developer account)

**Step 2:** Run `api_getter.py` with your client ID to get an API token
* Creates `token.json`
* If your API token expires, run `api_refresher.py`

**Step 3:** Run `get_anime_info.py`
* Requires `token.json`
* Writes the anime info to `animes.tsv`

**Step 4:** Run `binary_df.py` to clean and format the data from `animes.tsv` for training
* Writes the data to `training_data.tsv`

**Step 5** Run `recommender.py`