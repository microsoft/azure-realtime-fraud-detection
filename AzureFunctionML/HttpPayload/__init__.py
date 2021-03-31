import logging

import azure.functions as func
import json
import requests
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    url = os.getenv("AKSEndpoint")
    logging.info(url)
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.getenv("AKSKey")}'}

    logging.info(headers)

    data = json.loads(req.get_body())
    logging.info(data)
    
    payload = '{"name":0,"index":["type","amount","oldbalanceOrg","newbalanceOrig","oldbalanceDest","newbalanceDest","hour","dayOfMonth","isMerchantDest","errorBalanceOrig","errorBalanceDest"],"data":[3.0,1864.28,21249.0,19384.72,0.0,0.0,1.0,1.0,1.0,0.0,1864.28]}' 

    response = requests.request("POST", url, headers=headers, data= payload)


    return func.HttpResponse(response.text,status_code=200)
