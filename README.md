# Movie Recommendation System
# Step 1: Environment Setup

## 1.1 Set Up the Local Development Environment
1. Open your **VS Code** and create a new project folder.
2. Initialize a Python virtual environment by running the following commands in the terminal:

   ```bash
   # Navigate to your project folder
   cd your-project-folder

   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   ```
   
3. Install the necessary Python libraries:

   ```bash
    pip install pandas numpy scikit-learn flask azure-storage-blob pyspark
   ```

## 1.2 Set Up Azure Resources
1. Create Azure Data Lake Storage:
   Go to the Azure Portal and create a Storage Account with a Blob Container.Name the container 'movielensdata'.
2. Get the Connection String:
   In the Storage Account, under Security + Networking > Access keys, copy the connection string.
3. Install the Azure CLI:
   The Azure Command-Line Interface (CLI) is a cross-platform command-line tool that can be installed locally on Windows computers. You can use the Azure CLI for Windows to connect to Azure and execute administrative commands on Azure resources. The Azure CLI for       
   Windows can also be used from a browser through the Azure Cloud Shell or run from inside a Docker container.
  
  ```bash
   az login
   ```

  Choose the azure account when prompted, also choose the subscription.
 
# Step 2: Data Ingestion
## 2.1 Download the MovieLens Dataset
1. Go to the MovieLens Dataset page.
2. Download the MovieLens 25M Dataset.
3. Extract the dataset and place the movies.csv and ratings.csv files into our project folder.

## 2.2 Upload Data to Azure Data Lake
1. Create a python script 'uploadToAzure.py' to upload the MovieLens data set to the Azure container. Details like connection string, containere name and source path to be specified in the code.
2. Run the python script
```bash
python uploadToAzure.py
```
4. Verify the files in AZure container.

## 2.3 TMDB API Data Collection
1. Create a free account and request for api key.
2. Test TMDB API by fetching some metadata. Create a python script 'fetchTmdbMetadata.py' containing api key to fetch the metadata.
3. Run the script
```bash
python fetchTmdbMetadata.py
```
4. Verify the metadata is printed.

# Step 3: Ingest and Transform Data
## 3.1 Ingest MovieLens Data
1. Load the movie.csv and ratings.csv datasets into Panda Dataframes from Azure Blob Storage using script 'ingestMovieLensData.py'
2. Run the script.
   
```bash
python .\ingestMovieLensDataPD.py
```
3. Verify that csv are dowloaded to \data folder.

## 3.2 Enhance the data with TMDB Metadata
1. Let us add Genres, Popularity and Overview columns to the data.
2. Python script 'enhanceData' created to enhance the data and save it as enriched_movie.csv.
