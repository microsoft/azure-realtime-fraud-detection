from azure.cosmos import exceptions, CosmosClient, PartitionKey

# Initialize the Cosmos client
endpoint = "https://cosmosdb-tesserato-fraud.documents.azure.com:443/"
key = 'IWooseGq5mHA14FYhVga0cD2GRUaFxGYIgkWZHpAa7iKzp1XYp07SUfsNnUdkpYaVWFJKOqbU81CHaJHgRCe9w=='


client = CosmosClient(endpoint, key)

database_name = 'Fraud'
database = client.create_database_if_not_exists(id=database_name)
container_name = 'users'

query = "SELECT * FROM c WHERE c.CustomerId = 3319" 

items = list(container.query_items(
    query=query,
    enable_cross_partition_query=True
))

request_charge = container.client_connection.last_response_headers['x-ms-request-charge']








