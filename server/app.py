import csv
import pickle
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / 'data'
MODEL_PATH = DATA_DIR / 'model.pkl'
AIRPORTS_PATH = DATA_DIR / 'airports.csv'

with MODEL_PATH.open('rb') as handle:
    model = pickle.load(handle)


def _load_airports():
    with AIRPORTS_PATH.open(newline='') as handle:
        reader = csv.DictReader(handle)
        airports = [
            {'id': int(row['id']), 'name': row['name']}
            for row in reader
        ]
    return sorted(airports, key=lambda item: item['name'])


def _delay_probability(day_of_week, airport_id):
    key = (int(day_of_week), int(airport_id))
    if key in model:
        return float(model[key])

    day_values = [value for (day, _), value in model.items() if day == int(day_of_week)]
    if day_values:
        return float(sum(day_values) / len(day_values))
    return 0.0


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response


@app.route('/predict', methods=['GET'])
def predict():
    day_of_week = int(request.args.get('day_of_week', 1))
    airport_id = int(request.args.get('airport_id', 0))
    delay = _delay_probability(day_of_week, airport_id)
    certainty = min(1.0, max(0.0, abs(delay - 0.5) * 2.0))
    return jsonify({'certainty': certainty, 'delay': delay})


@app.route('/airports', methods=['GET'])
def airports():
    return jsonify(_load_airports())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
