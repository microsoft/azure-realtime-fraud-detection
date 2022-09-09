import joblib
import json
import pandas as pd
import os
import time
import random
from datetime import datetime

# Called when the deployed service starts
def init():
    global model

    print('PATH: ', os.path.join(os.getenv('AZUREML_MODEL_DIR')))
    # Get the path where the deployed model can be found.
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), './output-model/best_model.joblib')
    
    # Load model
    model = joblib.load(model_path)

# Handle requests to the service
def run(data):
  input_data = json.loads(data)
  input_data = pd.DataFrame([input_data])
  
  # Return the prediction
  prediction = predict(input_data)
  
  #end_time = datetime.now()
  #diff_time = end_time - current_time
  #prediction.update({'elapsed_time': diff_time.microseconds / 1000})
  
  return prediction

def predict(data):
  prediction = model.predict(data)[0]
  return {"prediction": str(prediction)}