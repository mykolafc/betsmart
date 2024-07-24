from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
import time
import pandas as pd

app = Flask(__name__)
CORS(app)


@app.route('/data', methods=['GET'])
def get_data():
    df = pd.read_csv('bin/combined.csv')  # Read your dataframe from a CSV file
    df = df.replace({np.nan: None})
    # Convert DataFrame back to a dictionary
    data_cleaned = df.to_dict(orient='records')
    return jsonify(data_cleaned)


if __name__ == '__main__':
    app.run(debug=True)
