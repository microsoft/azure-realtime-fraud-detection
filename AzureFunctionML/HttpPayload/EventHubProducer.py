import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

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

loop = asyncio.get_event_loop()
loop.run_until_complete(run())