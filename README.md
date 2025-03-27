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
   Go to the Azure Portal and create a Storage Account with a Blob Container.Name the container 'bronze'.
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

# Step 3: Set Up Azure Databricks Environment

## 3.1 Create a Databricks Workspace
1. Go to the Azure portal and create a Databricks Workspace.
2. Launch the Databricks environment.
3. Create a Cluster:In the Databricks workspace, create a cluster with the appropriate configuration.
   
## 3.2  Access Data Lake Using Azure Key Vault
1. Create a Microsoft Entra ID service principal.
2. Create a client secret for the service principal
3. Grant the service principal access to Azure Data Lake Storage.

# Step 4: Analyse and Clean Data Using Databricks

## 4.1 Connect to Azure Data Lake Storage using python
1. Create a new folder in the Workspace.
2. Inside the folder create a notebook.
3. Connect to ADLS using the python script. 
    
    ```python
    service_credential = dbutils.secrets.get(scope="<scope>",key="<service-credential-key>")

    spark.conf.set("fs.azure.account.auth.type.<storage-account>.dfs.core.windows.net", "OAuth")
    spark.conf.set("fs.azure.account.oauth.provider.type.<storage-account>.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
    spark.conf.set("fs.azure.account.oauth2.client.id.<storage-account>.dfs.core.windows.net", "<application-id>")
    spark.conf.set("fs.azure.account.oauth2.client.secret.<storage-account>.dfs.core.windows.net", service_credential)
    spark.conf.set("fs.azure.account.oauth2.client.endpoint.<storage-account>.dfs.core.windows.net", "https://login.microsoftonline.com/<directory-id>/oauth2/token")
    ```
4. Do the neccessary cleaning in Databricks and load the csv to the Silver container(MovieLensDataCleaningDatabricks.ipynb)
     
# Step 5: Enhance the cleaned data with TMDB Metadata (Using VS CODE)
## 5.1 Load Cleaned Data from Azure Blob Storage
1. Load the cleaned movielens.csv and ratings.csv datasets into Panda Dataframes from Azure Blob Storage using script 'ingestMovieLensData.py'
2. Run the script.
   
```bash
python .\ingestMovieLensDataPD.py
```
3. Verify that csv are dowloaded to \data folder.

## 5.3 Enhance the data with TMDB Metadata
1. Let us add Genres, Popularity and Overview columns to the data.
2. Run the script 'ingestMovieLensData.py'.
3. Verify 

# Step 5: Enhance the cleaned data with TMDB Metadata (Using Databricks)

## 5.1 Load Cleaned Data from Azure Blob Storagea
## 5.2 Enhance the cleaned data with TMDB Metadata
1. Define a UDF for Metadata Fetching.
2. Parse the Metadata into Separate Columns.
3. Save Enriched Data to Azure Blob Storage Gold Layer.
4. Verify


# Step 6: Build the model
1. Load the files movies and ratings from gold container to dataframe.
2. Split the data into training and testing sets.
3. Train a Singular Value Decomposition (SVD) model using the training set.
4. Evaluate the model's performance on the test set using Root Mean Squared Error (RMSE).
5. Generate top-N recommendations for a specific user.