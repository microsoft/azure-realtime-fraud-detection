from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import traceback
import enum
import os

class FraudRing():
    
    def __init__(self):
        gremlin_client = self._connect_gremlin_(client)
        return gremlin_client

    def _connect_gremlin_(self, client):
        self.client = client.Client(os.getenv("HOST_GREMLIN"), 'g',
                           username="/dbs/{}/colls/{}".format(os.getenv("DB_GREMLIN"), os.getenv("CONTAINER_GREMLIN")),
                           password=os.getenv("KEY_GREMLIN"),
                           message_serializer=serializer.GraphSONSerializersV2d0()
                           )
    
    def insert_vertice(self, id):        
        customer_data = self._get_customer_data_(id)
        node_property = self._add_property_(id, customer_data)
        add_vertice = self._mount_add_vertice_('person', node_property)

        try:
            self._execute_gremlin_command_(add_vertice)
            print('Added Vertice successful')
        except GremlinServerError as e:
            # When the vertex already exists we must update it
            if e.status_attributes["x-ms-status-code"] == 409:
                print('Conflict error!')
                update_vertice = self._mount_update_vertice_(id, node_property)
                self._execute_gremlin_command_(update_vertice)
                print('Updated Vertice successful')
        return customer_data
    
    def insert_edge(self, customeridOrig, customeridDest, type, prediction, customer_data_Orig, customer_data_Dest):
        add_edge = self._mount_edge_(customeridOrig,
                                         customeridDest,
                                         type,
                                         prediction,
                                         customer_data_Orig,
                                         customer_data_Dest
                                         )
        
        try:
            self._execute_gremlin_command_(add_edge)
            print('Added Edge successful')
        except GremlinServerError as e:
            print("Something went wrong with this query: {0}".format(add_edge))

    def _execute_gremlin_command_(self, command):
        callback = self.client.submitAsync(command)
        if callback.result() is not None:
            print(f"\tThe command {command} was succesfull performed:\n\t{0}".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query: {0}".format(command))
        print("\n")
    
    def _add_property_(self, id, customer_data):
        properties = f".property('id', '{id}')"
        # customer_data = self._get_customer_data_(id)
        
        properties += f".property('first_name', '{customer_data['FirstName']}')"
        properties += f".property('last_name', '{customer_data['LastName']}')"
        
        return properties
    
    
    def _mount_add_vertice_(self, entity, node_properties):
        add_vertice = f"g.addV('{entity}'){node_properties}.property('pk', 'pk')"
        return add_vertice

    def _mount_edge_(self, customeridOrig, customeridDest, type, prediction, customer_data_Orig, customer_data_Dest):         
        properties_Orig = f".property('name_customeridOrig', '{customer_data_Orig['FirstName'] + ' ' + customer_data_Orig['LastName']}')"
        properties_Dest = f".property('name_customeridDest', '{customer_data_Dest['FirstName'] + ' ' + customer_data_Dest['LastName']}')"
        
        add_edge = f"g.V('{customeridOrig}').addE('{type}').to(g.V('{customeridDest}')).property('status', '{ 'Fraud' if prediction else 'OK'}')" 
        add_edge += properties_Orig
        add_edge += properties_Dest
        return add_edge

    def _mount_update_vertice_(self, vertice_id, node_properties):
        node_properties = node_properties.replace(f".property('id', '{vertice_id}')", '')
        update_vertice = f"g.V('{vertice_id}'){node_properties}"
        return update_vertice

    def _get_customer_data_(self,id):
        # Initialize the Cosmos client
        ##### Adicionar dentro do arquivo de config
        os.getenv("DB_GREMLIN")

        endpoint = os.getenv("cosmosdbfraud_customer_DOCUMENTDB")
        key = os.getenv("cosmosdbfraud_customer_DOCUMENTDB_Key")
        
        client = CosmosClient(endpoint, key)

        ##### Adicionar dentro do arquivo de config
        database_name = os.getenv("DATABASE_CUSTOMER")
        database = client.create_database_if_not_exists(id=database_name)
        container_name = os.getenv("CONTAINER_CUSTOMER")

        container = database.create_container_if_not_exists(
        id=container_name, 
        partition_key=PartitionKey(path="/CustomerId"),
        offer_throughput=400)

        query = "SELECT * FROM c WHERE c.CustomerId = '" + str(id) + "'" 

        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        return items[0]

    def edge_operation(self, type_id):
        switcher={
            1: "TRANSFER_TO",
            2: "PAYMENT",
            3: "DEPOSIT"
        }
        return switcher.get(type_id,"Invalid day of week")
        
    
if __name__ == "__main__":
    fr = FraudRing()
    client = fr.connect_gremlin(client)

    _gremlin_insert_vertices = _gremlin_insert_vertices = [
        "g.addV('person').property('id', 'teste-01').property('firstName', 'Thomas').property('lastName', 'Marc').property('age', 44).property('pk', 'pk')",
    ]

    _gremlin_update_vertices = [
        "g.V('thomas').property('age', 44)"
    ]

    try:
        fr.insert_vertices(client)
        print('Added successful')
    except GremlinServerError as e:
        # When the vertex already exists we must update it
        if e.status_attributes["x-ms-status-code"] == 409:
            print('Conflict error!')
            fr.update_vertices(client)
