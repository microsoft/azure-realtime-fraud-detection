import logging

import azure.functions as func
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import datetime
import os

async def main(req: func.HttpRequest) -> func.HttpResponse:
    topic_raw_payload = os.getenv("EventHubTopic")
    eventhub_namespace = os.getenv("EventHubConnectionString")
    req_body = req.get_json()
    
    if req_body:
        await produceMessage(req_body,topic_raw_payload,eventhub_namespace)
        return func.HttpResponse(f"Hello. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )


async def produceMessage(event,topic,namespaceConnectionString):
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.

    producer = EventHubProducerClient.from_connection_string(conn_str=namespaceConnectionString, eventhub_name=topic)
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        event_data_batch.add(EventData(event))
        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)
        logging.info('Mensagem inserida com sucesso')

    # comment this but we need to test de retry even have a failure to send a message.
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(produceMessage(payload,topic_raw_payload,eventhub_namespace))



'''
def main(req: func.HttpRequest):
    timestamp = datetime.datetime.utcnow()
    logging.info('Message created at: %s', timestamp)
    req_body = req.get_json()

    return str(req_body)

'''



