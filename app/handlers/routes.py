import this
from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os

def configure_routes(app):

    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    model = joblib.load(model_path)

    @app.route('/')
    def hello():
        return "try the predict route it is great!"

    @app.route('/predict', methods=['POST'])
    def predict():
        """
        Below is an example POST request using curl:
            curl -X 'POST' '127.0.0.1:5000/predict' -H 'accept: application/json' \
                -H 'Content-Type: application/json' -d \
                    '{"school": "GP",
                      "traveltime": 4,
                      "studytime": 4,
                      "failures": 4,
                      "paid": "yes",
                      "activities": "yes",
                      "nursery": "yes",
                      "higher": "yes",
                      "internet": "yes",
                      "freetime": 5,
                      "goout": 5,
                      "Dalc": 5,
                      "Walc": 5,
                      "health": 5,
                      "absences": 93}'
        """
        if request.method == 'POST':
            json_data = request.get_json()
            df = pd.json_normalize(json_data)
            yesno_cols = ['paid','activities','nursery','higher','internet']
            school_col = ['school']
            df_num = df[df.columns.difference(yesno_cols)]
            df_yesno = pd.get_dummies(df[yesno_cols].astype(pd.CategoricalDtype(categories=['yes','no'])))
            df_school = pd.get_dummies(df[school_col].astype(pd.CategoricalDtype(categories=['GP','MS'])))
            df_processed = df_num.join(df_yesno).join(df_school)
            column_list = ['Dalc', 'Walc', 'absences', 'failures', 'freetime', 'goout', 'health', 'studytime', 'traveltime', 'activities_no', 'activities_yes', 'higher_no', 'higher_yes', 'internet_no', 'internet_yes', 'nursery_no', 'nursery_yes', 'paid_no', 'paid_yes', 'school_GP', 'school_MS']
            df_processed = df_processed[column_list]
            result = int(model.predict(df_processed)[0])
            return jsonify({'prediction': result})
