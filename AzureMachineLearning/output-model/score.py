import joblib
import json
import pandas as pd
import numpy as np
import os
import time
import random
from datetime import datetime
from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType

# Called when the deployed service starts
def init():
    global model

    # Get the path where the deployed model can be found.
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), './output-model/best_model.joblib')
    
    # Load model
    model = joblib.load(model_path)

input_sample = pd.DataFrame(data=[{"type":1.0,
                                   "amount":100.00,
                                   "oldbalanceOrg":1000.0,
                                   "newbalanceOrig": 900.00,
                                   "oldbalanceDest":0.0,
                                   "newbalanceDest":0.0,
                                   "hour":1.0,
                                   "dayOfMonth":1.0,
                                   "isMerchantDest":1.0,
                                   "errorBalanceOrig":0.0,
                                   "errorBalanceDest":900.00}])
pandas_sample_input = PandasParameterType(input_sample)

# This is an integer type sample. Use the data type that reflects the expected result.
output_sample = np.array([0])

@input_schema('data', pandas_sample_input)
@output_schema(NumpyParameterType(output_sample))
# Handle requests to the service
def run(data):
  prediction = predict(data)
  
  #end_time = datetime.now()
  #diff_time = end_time - current_time
  #prediction.update({'elapsed_time': diff_time.microseconds / 1000})
  
  return prediction

def predict(data):
  prediction = model.predict(data)[0]
  return {"prediction": str(prediction)}