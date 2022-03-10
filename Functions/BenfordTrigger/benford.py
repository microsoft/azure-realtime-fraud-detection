from azure.cosmos import CosmosClient, PartitionKey
import traceback
import enum
import os

class Benford():
    
    def __init__(self):
        cosmosdb_client = self._connect_cosmosdb_()
        return cosmosdb_client

    def _connect_cosmosdb_(self):
        self.endpoint = os.getenv("HOST_BENFORD")
        self.key = os.getenv("KEY_BENFORD")
        print("ESTAS SÃO AS CHAVES:", self.endpoint, self.key)
        self.client = CosmosClient(self.endpoint, self.key)

        ##### Adicionar dentro do arquivo de config
        self.database_name = os.getenv("DB_BENFORD")
        print("ESTE É O BD:", self.database_name)
        self.database = self.client.create_database_if_not_exists(id=self.database_name)
    
    def _return_container_(self, container_name):
        container = self.database.create_container_if_not_exists(
                                    id=container_name, 
                                    partition_key=PartitionKey(path="/digit_number"),
                                    offer_throughput=400)
        
        return container
    
    def _query_db_(self, container, query):
        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        return items[0]

    def _replace_db_item_(self, container, doc_id, type):
        print('\n1.5 Replace an Item\n')

        read_item = container.read_item(item=doc_id, partition_key=doc_id)
        read_item['digit_count'] = read_item['digit_count'] + 1
        digit_total = self._query_db_(container, "SELECT VALUE SUM(c.digit_count) FROM c ") + 1
        read_item['digit_percent'] = read_item['digit_count'] / (digit_total)
        response = container.replace_item(item=read_item, body=read_item)

        # Update all collection
        for digit in range(1 if type=="first-digit" else 0, 9):
            if(digit != int(doc_id)):
                read_item = container.read_item(item=str(digit), partition_key=str(digit))
                read_item['digit_percent'] = read_item['digit_count'] / digit_total
                response = container.replace_item(item=read_item, body=read_item)

        print('Replaced Item\'s Id is {0}, new subtotal={1}'.format(response['id'], response['digit_count']))
    
    def calculate_benford(self, documents):
        container = self._return_container_('Benford-First-Digit')

        # Calculate first-digit
        first_digit = str(documents[0]['amount'])[0]
        self._replace_db_item_(container, first_digit, "first-digit")
        
        # Calculate second-digit
        container = self._return_container_('Benford-Second-Digit')
        second_digit = str(documents[0]['amount'])[1]
        self._replace_db_item_(container, second_digit, "second-digit")