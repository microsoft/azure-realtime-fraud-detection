from locust import HttpUser, task, between
import json, os, random

hostname = os.getenv('url')
api_key = os.getenv('api_key') # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}


# Creating an API User class inheriting from Locust's HttpUser class
class APIUser(HttpUser):
    wait_time = between(1, 2)

    # Defining the post task using the JSON test data
    @task()
    def predict_endpoint(self):
        template_body = { 
    "customeridOrig":77, 
    "type":2,
    "amount":200,
    "oldbalanceOrg":200,
    "newbalanceOrig": 0,
    "customeridDest":76, 
    "oldbalanceDest":0,
    "newbalanceDest":100,
    "hour":1,
    "dayOfMonth":1,
    "isMerchantDest":1,
    "errorBalanceOrig":0,
    "errorBalanceDest":3000
}

        payload = self.return_random_body(template_body)
        self.client.post('/', json = payload, headers=headers)

    def return_random_body(self, template_body):
        template_body.update({"customeridOrig": int(random.uniform(1, 1000))})
        template_body.update({"customeridDest": int(random.uniform(1001, 2000))})
        template_body.update({"amount": random.uniform(10, 100)})
        template_body.update({"type": int(random.uniform(1, 3))})
        return template_body
