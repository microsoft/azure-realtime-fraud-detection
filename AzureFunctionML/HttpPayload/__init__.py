import logging

import azure.functions as func
import json
import requests
import os
import asyncio

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    url = os.getenv("AKSEndpoint")

    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.getenv("AKSKey")}'}

    data = json.loads(req.get_body())
    
    #payload = '{"name":0,"index":["type","amount","oldbalanceOrg","newbalanceOrig","oldbalanceDest","newbalanceDest","hour","dayOfMonth","isMerchantDest","errorBalanceOrig","errorBalanceDest"],"data":[3.0,1864.28,21249.0,19384.72,0.0,0.0,1.0,1.0,1.0,0.0,1864.28]}' 

    response = requests.request("POST", url, headers=headers, data= json.dumps(data))
    #alterar prediction
    data.update({"prediction" : response.json()['prediction'][1]})
    
    #send to eventHub
    requests.request("POST", "http://localhost:7071/api/EventHubHttpTrigger", headers=headers, data= json.dumps(data))


    return func.HttpResponse(response.text,status_code=200)
    
