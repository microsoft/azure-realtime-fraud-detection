import urllib.request
import json
import os
import ssl

data = {"customeridOrig":1, 
        "type":3,
        "amount":100,
        "oldbalanceOrg":100,
        "newbalanceOrig": 0,
        "customeridDest":2, 
        "oldbalanceDest":0,
        "newbalanceDest":100,
        "hour":1,
        "dayOfMonth":1,
        "isMerchantDest":1,
        "errorBalanceOrig":0,
        "errorBalanceDest":3000}

body = str.encode(json.dumps(data))

url = os.getenv('url')
api_key = os.getenv('api_key') # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    print(error.info())
    print(json.loads(error.read().decode("utf8", 'ignore')))

def request_api(url, body, headers):
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        print(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))

#request_api(url, api_key, headers)
