import logging

import sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ))))

import azure.functions as func
import json
import requests
import os
import asyncio
import typing
import config


def main(req: func.HttpRequest, msg: func.Out[str]) -> func.HttpResponse:
    url = os.getenv("AKSEndpoint")
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.getenv("AKSKey")}'}

    data = json.loads(req.get_body())
    data_prediction = dict((k, data[k]) for k in config.prediction_columns if k in data)
    data_prediction = {"data": [data_prediction]}

    response = requests.request("POST", url, headers=headers, data= json.dumps(data_prediction))
    data.update({"prediction" : response.json()['prediction'][0]})
    msg.set(json.dumps(data))

    return func.HttpResponse(response.text,status_code=200)