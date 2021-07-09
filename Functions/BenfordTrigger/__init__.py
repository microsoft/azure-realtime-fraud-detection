import logging
import sys, os

import azure.functions as func

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ))))

from benford import Benford


def main(documents: func.DocumentList) -> str:
    if documents:
        benford = Benford()
        benford.calculate_benford(documents)

        logging.info('Document id: %s', documents[0]['id'])
