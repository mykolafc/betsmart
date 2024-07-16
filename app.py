from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)


@app.route('/data', methods=['GET'])
def get_data():
    df = pd.read_csv('bin\combined.csv')  # Read your dataframe from a CSV file
    data = df.to_dict(orient='records')  # Convert dataframe to dictionary
    return jsonify(data)  # Return the data as JSON


if __name__ == '__main__':
    app.run(debug=True)
