import pandas as pd
import requests
from azure.storage.blob import BlobServiceClient
from tqdm import tqdm
import time
from azure.core.exceptions import AzureError
import io

# Azure Blob Storage configuration
CONNECTION_STRING = """"""
CONTAINER_NAME = "silver"
MOVIES_BLOB_NAME = "movies/movielens"
RATINGS_BLOB_NAME = "ratings/ratings"
ENRICHED_MOVIES_BLOB_NAME = "enriched_movies.csv"

# TMDB API configuration
TMDB_API_KEY = ""
TMDB_BASE_URL = "https://api.themoviedb.org/3/search/movie"


def download_blob_to_dataframe(container_name, blob_name):
    """
    Download a blob from Azure Blob Storage and load it into a Pandas DataFrame.
    """
    # Initialize BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    
    # Get the BlobClient
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
    try:
        # Download the blob
        blob_data = blob_client.download_blob()
        content = blob_data.readall()  # Read all the data as bytes
        
        # Convert bytes to a StringIO object and load it into a Pandas DataFrame
        df = pd.read_csv(io.StringIO(content.decode("utf-8")),
        on_bad_lines="skip"  # Skips lines with issues
        )
        print(f"Downloaded blob '{blob_name}' successfully!")
        print(df.columns)
        return df
    except Exception as e:
        print(f"Failed to download blob '{blob_name}': {e}")
        raise



def fetch_movie_metadata(title):
    """
    Fetch movie metadata from the TMDB API.
    """
    params = {"api_key": TMDB_API_KEY, "query": title}
    try:
        response = requests.get(TMDB_BASE_URL, params=params)
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                metadata = results[0]
                return {
                    "overview": metadata.get("overview", ""),
                    "popularity": metadata.get("popularity", 0.0),
                    "release_date": metadata.get("release_date", ""),
                    "vote_average": metadata.get("vote_average", 0.0),
                    "vote_count": metadata.get("vote_count", 0),
                }
        return {"overview": "", "popularity": 0.0, "release_date": "", "vote_average": 0.0, "vote_count": 0}
    except Exception as e:
        print(f"Error fetching metadata for '{title}': {e}")
        return {"overview": "", "popularity": 0.0, "release_date": "", "vote_average": 0.0, "vote_count": 0}


def enrich_movies(movies_df):
    """
    Enrich the movies DataFrame with metadata from the TMDB API.
    """
    enriched_data = []
    for _, row in tqdm(movies_df.iterrows(), total=len(movies_df)):
        title = row["title"]
        metadata = fetch_movie_metadata(title)
        enriched_data.append({
            "movieId": row["movieId"],
            "title": title,
            "genres": row["genres"],
            "year": row["year"],
            "overview": metadata["overview"],
            "popularity": metadata["popularity"],
            "release_date": metadata["release_date"],
            "vote_average": metadata["vote_average"],
            "vote_count": metadata["vote_count"],
        })
        time.sleep(0.2)  # Prevent hitting API rate limits

    enriched_df = pd.DataFrame(enriched_data)
    return enriched_df


def upload_dataframe_to_blob(container_name, blob_name, dataframe):
    """
    Upload a pandas DataFrame to Azure Blob Storage as a CSV file.
    """
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    csv_data = dataframe.to_csv(index=False)
    blob_client.upload_blob(csv_data, overwrite=True)
    print(f"Uploaded {blob_name} successfully!")


def main():
    # Step 1: Download cleaned data from Azure Blob Storage
    movies_df = download_blob_to_dataframe(CONTAINER_NAME, MOVIES_BLOB_NAME)
    ratings_df = download_blob_to_dataframe(CONTAINER_NAME, RATINGS_BLOB_NAME)

    # Step 2: Enrich movies with TMDB metadata
    print("Enriching movies data with TMDB metadata...")
    enriched_movies_df = enrich_movies(movies_df)

    # Step 3: Save enriched data back to Azure Blob Storage
    upload_dataframe_to_blob(CONTAINER_NAME, ENRICHED_MOVIES_BLOB_NAME, enriched_movies_df)

    print("Enrichment process completed successfully!")


if __name__ == "__main__":
    main()
