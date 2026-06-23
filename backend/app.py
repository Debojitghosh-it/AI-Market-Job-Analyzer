from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

df = pd.read_csv("AI_Impact_on_Jobs_2030.csv")

@app.route("/")
def home():
    return jsonify(df.columns.tolist())

if __name__ == "__main__":
    app.run(debug=True)