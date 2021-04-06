import logging

import azure.functions as func
import json
import requests
import os
import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData



#initialize for global variables testing in Event Hub
data = ""
topic_raw_payload = ""
eventhub_namespace = ""
payload = ""

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    url = os.getenv("AKSEndpoint")
    global topic_raw_payload
    global eventhub_namespace

    topic_raw_payload = os.getenv("EventHubTopic")
    eventhub_namespace = os.getenv("EventHubConnectionString")
    logging.info(url)
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.getenv("AKSKey")}'}

    logging.info(headers)
    global data
    data = json.loads(req.get_body())
    #insert raw payload into EventHub

   
    logging.info(data)
    global payload
    payload = '{"name":0,"index":["type","amount","oldbalanceOrg","newbalanceOrig","oldbalanceDest","newbalanceDest","hour","dayOfMonth","isMerchantDest","errorBalanceOrig","errorBalanceDest"],"data":[3.0,1864.28,21249.0,19384.72,0.0,0.0,1.0,1.0,1.0,0.0,1864.28]}' 
    
    await produceMessage(payload,topic_raw_payload,eventhub_namespace)

    response = requests.request("POST", url, headers=headers, data= payload)

    return func.HttpResponse(response.text,status_code=200)

    
async def produceMessage(event,topic,namespaceConnectionString):
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.

    producer = EventHubProducerClient.from_connection_string(conn_str=namespaceConnectionString, eventhub_name=topic)
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        event_data_batch.add(EventData(payload))
        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)
        logging.info('Mensagem inserida com sucesso')

    # comment this but we need to test de retry even have a failure to send a message.
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(produceMessage(payload,topic_raw_payload,eventhub_namespace))
