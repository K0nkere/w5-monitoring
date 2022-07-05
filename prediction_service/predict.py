
import pickle
from flask import Flask, request, jsonify

with open('/home/kkr/notebooks/models/green_lin_reg.bin', 'rb') as f_in:
    dv, lr = pickle.load(f_in)

def prepare_features(ride):
    features = {
                "trip_distance": ride.get("trip_distance"),
                "PU_DO": "%s_%s" %(ride.get("PULocationID"), ride.get("DOLocationID")),
               }
    
    print(features)
    return features

def predict(features):
    X = dv.transform(features)
    predictions = lr.predict(X)
    return predictions

print('Green taxi predictor load successfully')

app = Flask('duration-prediction')

@app.route('/predict', methods = ['POST'])
def predict_endpoint():
    ride = request.get_json()
    
    features = prepare_features(ride)
    prediction = predict(features)
    
    result = {'duration': prediction[0]}
    print(result)
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port = 9696)
