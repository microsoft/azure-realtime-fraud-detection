import logging

import azure.functions as func

import sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ))))

from fraud_ring import FraudRing


def main(documents: func.DocumentList) -> str:
    print('receiving a document ...')
    if documents:
        fr = FraudRing()

        # Insert (or update) origin vertice
        fr.insert_vertice(documents[0]['customeridOrig'])

        # Insert (or update) destination vertice
        fr.insert_vertice(documents[0]['customeridDest'])


        # Correlation new edge
        fr.insert_edge(documents[0]['customeridOrig'], 
        documents[0]['customeridDest'], 
        "TRANSFER_TO", 
        documents[0]['prediction'])

        logging.info('Document id: %s', documents[0]['id'])
        

