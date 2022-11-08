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

    def _validate_df(df):
        assert(df["school"][0] in ["GP", "MS"])
        assert(1 <= df["traveltime"][0] <= 4)
        assert(1 <= df["studytime"][0] <= 4)
        assert(0 <= df["failures"][0] <= 4)
        assert(df["paid"][0] in ["yes", "no"])
        assert(df["activities"][0] in ["yes", "no"])
        assert(df["nursery"][0] in ["yes", "no"])
        assert(df["higher"][0] in ["yes", "no"])
        assert(df["internet"][0] in ["yes", "no"])
        assert(1 <= df["freetime"][0] <= 5)
        assert(1 <= df["goout"][0] <= 5)
        assert(1 <= df["Dalc"][0] <= 5)
        assert(1 <= df["Walc"][0] <= 5)
        assert(1 <= df["health"][0] <= 5)
        assert(0 <= df["absences"][0] <= 93)

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
            _validate_df(df)
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
