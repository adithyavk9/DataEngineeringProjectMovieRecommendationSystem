import requests

# TMDB API Key
api_key = ""

# Fetch movie details from TMDB APIfetchTmdbMetadata
def fetch_movie_metadata(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for movie ID {movie_id}")
        return None

# Example movie ID: Fight Club (ID: 550)
movie_metadata = fetch_movie_metadata(550)
print(movie_metadata)
