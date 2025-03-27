from azure.storage.blob import BlobServiceClient
import os

# Azure Storage connection string
connection_string = """"""
container_name = "bronze"

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Upload a file to Azure Blob Storage
def upload_to_azure(file_path, blob_name):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
        print(f"{blob_name} uploaded successfully.")

# Define the files to upload
data_files = {
    "movies.csv": os.path.join(r"C:\Users\AdithyaVK\Desktop\Projects\RecommendationSystem", "movies.csv"),
    "ratings.csv": os.path.join(r"C:\Users\AdithyaVK\Desktop\Projects\RecommendationSystem", "ratings.csv"),
}

# Upload files
for blob_name, file_path in data_files.items():
    upload_to_azure(file_path, blob_name)
