import logging

import azure.functions as func
import json
import requests
import os
import asyncio
import typing
import aiohttp
import asyncio
from aiohttp import ClientSession


async def main(req: func.HttpRequest, msg: func.Out[str]) -> func.HttpResponse:

    # #message = req.params.get('body')
    # url = os.getenv("AKSEndpoint")
    # headers = {
    # 'Content-Type': 'application/json',
    # 'Authorization': f'Bearer {os.getenv("AKSKey")}'}

    # data = json.loads(req.get_body())
    # response = requests.request("POST", url, headers=headers, data= json.dumps(data))
    # data.update({"prediction" : response.json()['prediction'][0]})
    # msg.set(json.dumps(data))

    # return func.HttpResponse(response.text,status_code=200)

# url_list = ["https://func-tesserato-models.azurewebsites.net/api/HttpRLD",
# "https://func-tesserato-models.azurewebsites.net/api/HttpRLD"]





