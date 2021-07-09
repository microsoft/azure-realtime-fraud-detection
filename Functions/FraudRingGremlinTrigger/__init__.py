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
        customer_data_Orig = fr.insert_vertice(documents[0]['customeridOrig'])

        # Insert (or update) destination vertice
        customer_data_Dest = fr.insert_vertice(documents[0]['customeridDest'])

        # Correlation new edge
        fr.insert_edge(documents[0]['customeridOrig'], 
                       documents[0]['customeridDest'], 
                       fr.edge_operation(documents[0]['type']), 
                       documents[0]['prediction'],
                       customer_data_Orig,
                       customer_data_Dest
                       )

        logging.info('Document id: %s', documents[0]['id'])
        print('customeridOrig: %s', documents[0]['customeridOrig'])
        

