from azure.cosmos import exceptions, CosmosClient, PartitionKey
import sample_data
import config

# Initialize the Cosmos client
endpoint = config.COSMOSDB_ENDPOINT
key = config.COSMOSDB_KEY

client = CosmosClient(endpoint, key)
print(client)

database_name = 'fraud-detection-sql-db'
database = client.create_database_if_not_exists(id=database_name)


def get_container(container_name):
    # Create a container
    container = database.create_container_if_not_exists(
        id=container_name, 
        partition_key=PartitionKey(path="/id"),
        offer_throughput=400
    )
    return container

def clean_container(container):
    for item in container.query_items(
        query='SELECT * FROM c',
        enable_cross_partition_query=True):

        container.delete_item(item, partition_key=item['id'])

def create_benford_first_digit(container):
    items_to_create = sample_data.get_benford_items('first-digit')
    for item in items_to_create:
        container.create_item(body=item)

def create_benford_second_digit(container):
    items_to_create = sample_data.get_benford_items('second-digit')
    for item in items_to_create:
        container.create_item(body=item)

def create_customer_items(container):
    items_to_create = sample_data.get_customer_items()
    for item in items_to_create:
        container.create_item(body=item)

if __name__ == "__main__":
    # Create Benford First Digit samples
    container = get_container('Benford-First-Digit')
    clean_container(container)
    create_benford_first_digit(container)

    # Create Benford Second Digit samples
    container = get_container('Benford-Second-Digit')
    clean_container(container)
    create_benford_second_digit(container)

    # Create Customer samples
    container = get_container('Customers')
    clean_container(container)
    create_customer_items(container)