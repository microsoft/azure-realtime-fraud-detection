from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
import sys
import traceback

_gremlin_cleanup_graph = "g.V().drop()"

_gremlin_insert_vertices = [
    "g.addV('person').property('id', 'joao').property('firstName', 'João').property('lastName', 'Aragão').property('age', 27).property('pk', 'pk')",
    "g.addV('person').property('id', 'rafaela').property('firstName', 'Rafaela').property('lastName', 'Silva').property('age', 39).property('pk', 'pk')",
    "g.addV('person').property('id', 'luiz').property('firstName', 'Luiz').property('lastName', 'Braz').property('pk', 'pk')",
    "g.addV('person').property('id', 'alfeu').property('firstName', 'Alfeu').property('lastName', 'Duran').property('pk', 'pk')",
    "g.addV('person').property('id', 'luiza').property('firstName', 'Luiza').property('lastName', 'Braz').property('pk', 'pk')",
    "g.addV('person').property('id', 'pedro').property('firstName', 'Pedro').property('lastName', 'Santos').property('gender', 'man').property('age', 50).property('pk', 'pk')",
    "g.addV('person').property('id', 'mariana').property('firstName', 'Mariana').property('lastName', 'Alves').property('gender', 'woman').property('age', 18).property('pk', 'pk')",
    "g.addV('person').property('id', 'leonardo').property('firstName', 'Leonardo').property('lastName', 'Pereira').property('age', 22).property('pk', 'pk')",
    "g.addV('person').property('id', 'marcos').property('firstName', 'Marcos').property('lastName', 'Tadeu').property('gender', 'man').property('age', 35).property('pk', 'pk')"
]

_gremlin_insert_edges = [
    "g.V('joao').addE('TRANSFERED_TO').to(g.V('rafaela')).property('status', 'ok')",
    "g.V('joao').addE('TRANSFERED_TO').to(g.V('luiz')).property('status', 'ok')",
    "g.V('luiz').addE('TRANSFERED_TO').to(g.V('luiza')).property('status', 'ok')",
    "g.V('mariana').addE('TRANSFERED_TO').to(g.V('rafaela')).property('status', 'ok')",
    "g.V('rafaela').addE('TRANSFERED_TO').to(g.V('leonardo')).property('status', 'ok')",
    "g.V('pedro').addE('TRANSFERED_TO').to(g.V('marcos')).property('status', 'ok')",
    "g.V('1').addE('TRANSFERED_TO').to(g.V('2')).property('status', 'ok').property('status2", 'possível_fraude'),
    #"g.V('Paul').addE('HAS_BOUGHT_AT').to(g.V('Just_Brew_It')).property('Fraud', 1)",
    #"g.V('Just_Brew_It').addE('HAS_BOUGHT_AT').to(g.V('ben')).property('Fraud', 0)"    
]

_gremlin_update_vertices = [
    "g.v('pedro').outE('TRANSFERED_TO').as('e').inV().has('id', 'marcos').select('e').property('status', 'fraud')"
]
_gremlin_count_vertices = "g.V().count()"

_gremlin_traversals = {
    "Get all persons older than 40": "g.V().hasLabel('person').has('age', gt(40)).values('firstName', 'age')",
    "Get all persons and their first name": "g.V().hasLabel('person').values('firstName')",
    "Get all persons sorted by first name": "g.V().hasLabel('person').order().by('firstName', incr).values('firstName')",
    "Get all persons that Thomas knows": "g.V('thomas').out('knows').hasLabel('person').values('firstName')",
    "People known by those who Thomas knows": "g.V('thomas').out('knows').hasLabel('person').out('knows').hasLabel('person').values('firstName')",
    "Get the path from Thomas to Robin": "g.V('thomas').repeat(out()).until(has('id', 'robin')).path().by('firstName')"
}

def print_status_attributes(result):
    # This logs the status attributes returned for successful requests.
    # See list of available response status attributes (headers) that Gremlin API can return:
    #     https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#headers
    #
    # These responses includes total request units charged and total server latency time.
    # 
    # IMPORTANT: Make sure to consume ALL results returend by cliient tothe final status attributes
    # for a request. Gremlin result are stream as a sequence of partial response messages
    # where the last response contents the complete status attributes set.
    #
    # This can be 
    print("\tResponse status_attributes:\n\t{0}".format(result.status_attributes))

def cleanup_graph(client):
    print("\n> {0}".format(
        _gremlin_cleanup_graph))
    callback = client.submitAsync(_gremlin_cleanup_graph)
    if callback.result() is not None:
        callback.result().all().result() 
    print("\n")
    print_status_attributes(callback.result())
    print("\n")

def insert_vertices(client):
    for query in _gremlin_insert_vertices:
        print("\n> {0}\n".format(query))
        callback = client.submitAsync(query)
        if callback.result() is not None:
            print("\tInserted this vertex:\n\t{0}".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query: {0}".format(query))
        print("\n")
        print_status_attributes(callback.result())
        print("\n")

    print("\n")

def insert_edges(client):
    for query in _gremlin_insert_edges:
        print("\n> {0}\n".format(query))
        callback = client.submitAsync(query)
        if callback.result() is not None:
            print("\tInserted this edge:\n\t{0}\n".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query:\n\t{0}".format(query))
        print_status_attributes(callback.result())
        print("\n")

    print("\n")

def update_vertices(client):
    for query in _gremlin_update_vertices:
        print("\n> {0}\n".format(query))
        callback = client.submitAsync(query)
        if callback.result() is not None:
            print("\tUpdated this vertex:\n\t{0}\n".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query:\n\t{0}".format(query))

        print_status_attributes(callback.result())
        print("\n")

    print("\n")

def count_vertices(client):
    print("\n> {0}".format(
        _gremlin_count_vertices))
    callback = client.submitAsync(_gremlin_count_vertices)
    if callback.result() is not None:
        print("\tCount of vertices: {0}".format(callback.result().all().result()))
    else:
        print("Something went wrong with this query: {0}".format(
            _gremlin_count_vertices))

    print("\n")
    print_status_attributes(callback.result())
    print("\n")


def execute_traversals(client):
    for key in _gremlin_traversals:
        print("{0}:".format(key))
        print("> {0}\n".format(
            _gremlin_traversals[key]))
        callback = client.submitAsync(_gremlin_traversals[key])
        for result in callback.result():
            print("\t{0}".format(str(result)))
        
        print("\n")
        print_status_attributes(callback.result())
        print("\n")

try:
    client = client.Client('wss://gremlin-tesserato-fraud.gremlin.cosmos.azure.com:443/', 'g',
                           username="/dbs/frauddetectiondb/colls/fraudring",
                           password="ZSKoarXkYHthkZYWAMUtYrGf1Q9shWgcCyjLrVJu8HZ7WFOcXXlHFqeInJq35mHDFloyMBM3I8cU1WMZpwYvPw==",
                           message_serializer=serializer.GraphSONSerializersV2d0()
                           )

    print("Welcome to Azure Cosmos DB + Gremlin on Python!")

    # Drop the entire Graph
    #input("We're about to drop whatever graph is on the server. Press any key to continue...")
    cleanup_graph(client)

    # Insert all vertices
    #input("Let's insert some vertices into the graph. Press any key to continue...")
    insert_vertices(client)

    # Create edges between vertices
    #input("Now, let's add some edges between the vertices. Press any key to continue...")
    insert_edges(client)

    # Update a couple of vertices
    #input("Ah, sorry. I made a mistake. Let's change the ages of these two vertices. Press any key to continue...")
    update_vertices(client)

    # Count all vertices
    #input("Okay. Let's count how many vertices we have. Press any key to continue...")
    count_vertices(client)

    # Execute traversals and get results
    #input("Cool! Let's run some traversals on our graph. Press any key to continue...")
    # execute_traversals(client)

    # Count all vertices again
    #input("How many vertices do we have left? Press any key to continue...")
    count_vertices(client)

except GremlinServerError as e:
    print('Code: {0}, Attributes: {1}'.format(e.status_code, e.status_attributes))

    # GremlinServerError.status_code returns the Gremlin protocol status code
    # These are broad status codes which can cover various scenaios, so for more specific
    # error handling we recommend using GremlinServerError.status_attributes['x-ms-status-code']
    # 
    # Below shows how to capture the Cosmos DB specific status code and perform specific error handling.
    # See detailed set status codes than can be returned here: https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#status-codes
    #
    # See also list of available response status attributes that Gremlin API can return:
    #     https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#headers
    cosmos_status_code = e.status_attributes["x-ms-status-code"]
    if cosmos_status_code == 409:
        print('Conflict error!')
    elif cosmos_status_code == 412:
        print('Precondition error!')
    elif cosmos_status_code == 429:
        print('Throttling error!');
    elif cosmos_status_code == 1009:
        print('Request timeout error!')
    else:
        print("Default error handling")

    traceback.print_exc(file=sys.stdout) 
    sys.exit(1)

print("\nAnd that's all! Sample complete")
