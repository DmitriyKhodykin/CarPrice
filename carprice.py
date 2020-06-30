# carprice.py

from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)


@app.route('/carprice', methods=['POST'])
def return_price():
    year = request.json.get('Year')
    driven = request.json.get('Driven(km)')
    transmission = request.json.get('Transmission')
    engine = request.json.get('Engine(cc)')
    power = request.json.get('Power(hp)')
    seats = request.json.get('Seats')

    with open('pickled_model.pkl', 'rb') as pkl_file:
        regressor = pickle.load(pkl_file)

    predict = regressor.predict([year, driven, transmission, engine, power, seats])
    return jsonify({'Predict Car Price, USD': round(predict * 1325, 1)})


if __name__ == '__main__':
    app.run('194.67.112.230', 5000)
