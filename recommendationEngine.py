import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
from azure.storage.blob import BlobServiceClient
import io

# Azure Blob Storage Configuration
CONNECTION_STRING = """"""
CONTAINER_NAME = "gold"
RATINGS_BLOB_NAME = "ratings/ratings"
MOVIES_BLOB_NAME = "movies/movies"

def download_blob_to_dataframe(container_name, blob_name):
    """
    Download a blob from Azure Blob Storage and load it into a Pandas DataFrame.
    """
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    try:
        # Download blob content
        blob_data = blob_client.download_blob()
        content = blob_data.readall()
        # Convert to Pandas DataFrame
        df = pd.read_csv(io.StringIO(content.decode("utf-8")))
        print(f"Downloaded '{blob_name}' successfully!")
        return df
    except Exception as e:
        print(f"Failed to download blob '{blob_name}': {e}")
        raise

# Step 1: Load Data from Azure Blob Storage
ratings_df = download_blob_to_dataframe(CONTAINER_NAME, RATINGS_BLOB_NAME)
movies_df = download_blob_to_dataframe(CONTAINER_NAME, MOVIES_BLOB_NAME)


# Step 2: Prepare Data for Surprise
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings_df[['userId', 'movieId', 'rating']], reader)

# Step 3: Train-Test Split
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# Step 4: Build and Train the Model
model = SVD()
model.fit(trainset)

# Step 5: Evaluate the Model
predictions = model.test(testset)
rmse = accuracy.rmse(predictions)
print(f"Root Mean Squared Error (RMSE): {rmse}")

movies_df.head(5)

# Step 6: Generate Recommendations
def get_top_n_recommendations(predictions, n=10):
    """
    Get top-N recommendations for each user from the predictions.
    """
    from collections import defaultdict
    top_n = defaultdict(list)

    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Sort the predictions for each user and retrieve the top N
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


# Get Top-10 Recommendations for Each User
top_n_recommendations = get_top_n_recommendations(predictions, n=10)

# Print Recommendations for a Sample User
sample_user_id = 1
print(f"Top-10 Recommendations for User {sample_user_id}:")

for movie_id, rating in top_n_recommendations[sample_user_id]:
    # Ensure movie_id and movies_df['movieId'] are of the same type
    movie_id = str(movie_id)  # Convert movie_id to string
    movie_row = movies_df[movies_df['movieId'] == movie_id]

    # Safely handle missing titles
    if not movie_row.empty:
        movie_title = movie_row['title'].values[0]
    else:
        movie_title = f"Unknown Movie (ID: {movie_id})"

    print(f"Movie: {movie_title}, Predicted Rating: {rating}")
