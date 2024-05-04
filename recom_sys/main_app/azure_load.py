from azure.storage.blob import BlobServiceClient
import csv
import os

file_path = os.path.abspath(__file__)
file_dir = os.path.dirname(file_path)
cust_info_path = os.path.join(file_dir, 'static', 'cust_info.csv')
product_info_path = os.path.join(file_dir, 'static', 'prod_info.csv')

# Connect to Azure Storage
connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
print(connection_string)
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Download CSV file from Azure Storage
container_name = "bin"
blob_name_1 = "cust_info.csv"
blob_name_2 = "prod_info.csv"
blob_client_1 = blob_service_client.get_blob_client(container=container_name, blob=blob_name_1)
blob_client_2 = blob_service_client.get_blob_client(container=container_name, blob=blob_name_2)
with open(cust_info_path, "wb") as f:
    f.write(blob_client_1.download_blob().readall())
with open(product_info_path, "wb") as f:
    f.write(blob_client_2.download_blob().readall())


