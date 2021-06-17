from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
import traceback
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
        
        node_property = self._add_property_id_(id)
        add_vertice = self._mount_add_vertice_('person', node_property)
        try:
            self._execute_gremlin_command_(add_vertice)
            print('Added Vertice successful')
        except GremlinServerError as e:
            # When the vertex already exists we must update it
            if e.status_attributes["x-ms-status-code"] == 409:
                print('Conflict error!')
                # update_vertice = self._mount_update_vertice_(id, node_property)
                # self._execute_gremlin_command_(update_vertice)
                print('Updated Vertice successful')
    
    def insert_edge(self, payload):
        add_edge = self._mount_add_edge_(payload['customeridOrig'],
                                         payload['customeridDest'],
                                         'TRANSFER_TO',
                                         payload['prediction']
        )

        try:
            self._execute_gremlin_command_(add_edge)
            print('Added Edge successful')
        except GremlinServerError as e:
            print("Something went wrong with this query: {0}".format(payload))

    def _execute_gremlin_command_(self, command):
        callback = self.client.submitAsync(command)
        if callback.result() is not None:
            print(f"\tThe command {command} was succesfull performed:\n\t{0}".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query: {0}".format(command))
        print("\n")
    
    def _add_property_id_(self, id):
        return f".property('id', '{id}')"
    
    def _mount_add_vertice_(self, entity, node_properties):
        add_vertice = f"g.addV('{entity}'){node_properties}.property('pk', 'pk')"
        return add_vertice

    def _mount_edge_(self, customer_origin, customer_dest, type, is_fraud):
         add_edge = f"g.V('{customer_origin}').addE('{type}').to(g.V('{customer_dest}')).property('status', {is_fraud})"
         return add_edge

    def _mount_update_vertice_(self, vertice_id, node_properties):
        node_properties = node_properties.replace(f".property('id', '{vertice_id}')", '')
        update_vertice = f"g.V('{vertice_id}'){node_properties}"
        return update_vertice


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
