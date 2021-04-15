import logging

import azure.functions as func
import json
import requests
import os
import asyncio
import typing


def main(req: func.HttpRequest, msg: func.Out[str]) -> func.HttpResponse:
    #message = req.params.get('body')
    url = os.getenv("AKSEndpoint")
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.getenv("AKSKey")}'}

    data = json.loads(req.get_body())
    response = requests.request("POST", url, headers=headers, data= json.dumps(data))
    data.update({"prediction" : response.json()['prediction'][1]})
    msg.set(json.dumps(data))

    return func.HttpResponse(response.text,status_code=200)