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
3. Install the necessary Python libraries:

   ```bash
    pip install pandas numpy scikit-learn flask azure-storage-blob pyspark

## 1.2 Set Up Azure Resources
1. Create Azure Data Lake Storage:
   Go to the Azure Portal and create a Storage Account with a Blob Container.Name your container 'movielensdata'.

2. Get the Connection String:
   In the Storage Account, under Security + Networking > Access keys, copy the connection string.

3. Install the Azure CLI:
   The Azure Command-Line Interface (CLI) is a cross-platform command-line tool that can be installed locally on Windows computers. You can use the Azure CLI for Windows to connect to Azure and execute administrative commands on Azure resources. The Azure CLI for Windows   
   can also be used from a browser through the Azure Cloud Shell or run from inside a Docker container.
  
  ```bash
   az login
   Choose the azure account when prompted also choose the subscription.

