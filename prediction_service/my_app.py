import os
import pickle

import requests
from flask import Flask, request, jsonify

from pymongo import MongoClient


MODEL_FILE = os.getenv('MODEL_FILE', 'lin_reg.bin')
MONGODB_ADDRESS = os.getenv('MONGODB_ADDRESS', 'mongodb://127.0.0.1:27017')
EVIDENTLY_SERVICE_ADDRESS = os.getenv('EVIDENTLY_SERVICE_ADDRESS', 'http://127.0.0.1:5000')
with open(MODEL_FILE,'rb') as f_in:
    dv, lr = pickle.load(f_in)
app = Flask('Duration')

mongo_client = MongoClient(MONGODB_ADDRESS)

db = mongo_client.get_database('prediction_service')
collection = db.get_collection('data')

@app.route('/predict', methods = ['POST'])
def predict():
    
    ride = request.get_json()
    
    record = {}
    record['PU_DO'] = '{:}_{:}'.format(ride.get('PULocation'), ride.get('DOLocation'))
    
    X = dv.transform([record])
    y_pred = lr.predict(X)
    
    result = {
        'duration':float(y_pred)
    }
    
    save_to_db(record, y_pred) # prediction -> y_pred
    save_to_evidently_service(record, y_pred) # prediction ->y_pred
    
    return jsonify(result)

def save_to_db(record, prediction):
    rec = record.copy()
    rec['prediction'] = prediction
    
    collectin.insert_one(rec)

def save_to_evidently_service(record, prediction):
    rec = record.copy()
    rec['prediction'] = prediction
    requests.post(f'{EVIDENTLY_SERVICE_ADDRESS}/iterate/taxi', json(rec))

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 9696)
