from os import getenv
from dotenv import load_dotenv
BASE_URL = "https://api.themoviedb.org/3/"
load_dotenv()
API_KEY = getenv("API_KEY")
MOVIE_SEARCH_ENDPOINT = 'search/movie'
MOVIE_DETAILS_ENDPOINT = 'movie/'
MOVIE_PROVIDERS_ENDPOINT ='/watch/providers'
headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
    }
