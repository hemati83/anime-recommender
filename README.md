# anime-recommender

**Step 1:** Apply for a myanimelist client ID (developer account)
* I'm not allowed to give mine out so if you want to run `api_getter.py`, you have to apply for your own ID

**Step 2:** Run `api_getter.py` with your client ID to get an API token
* Creates `token.json`
* If your API token expires, run `api_refresher.py`

**Step 3:** Run `get_anime_info.py`
* Requires `token.json`
* Writes the anime info to `animes.tsv`
* Note that this may take a while depending on how much data you want (roughly 3 minutes per 100 anime series)

**Step 4:** Run `binary_df.py` to clean and format the data from `animes.tsv` for training
* Requires `animes.tsv`
* Writes the data to `training_data.tsv`

**Step 5** Run `recommender.py`
* Requires `animes.tsv` and `training_data.tsv`

**Extra**
* In the event that you do not have a myanimelist client ID, I've included data from 2500 different anime series