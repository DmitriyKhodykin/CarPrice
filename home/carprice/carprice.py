# carprice.py

# Imports
from flask import Flask, request, jsonify
import pickle
import json

app = Flask(__name__)  # class initiation

# Handler
@app.route('/carprice', methods=['GET'])
def return_price():
    data = request.data
    data_dict = json.loads(data)
    year = data_dict['Year']
    driven = data_dict['Driven(km)']
    transmission = data_dict['Transmission']
    engine = data_dict['Engine(cc)']
    power = data_dict['Power(hp)']
    seats = data_dict['Seats']
    # Deserialization CatBoostReg
    with open('pickled_model.pkl', 'rb') as pkl_file:
        regressor = pickle.load(pkl_file)

    predict = regressor.predict([year, driven, transmission, engine, power, seats])
    return jsonify({'Predict Car Price, USD': round(predict * 1325, 1)})


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
