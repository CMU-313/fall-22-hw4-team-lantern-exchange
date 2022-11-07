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


    # @app.route('/predict')
    # def predict():
    #     #use entries from the query string here but could also use json
    #     age = request.args.get('age')
    #     absences = request.args.get('absences')
    #     health = request.args.get('health')
    #     data = [[age], [health], [absences]]
    #     query_df = pd.DataFrame({
    #         'age': pd.Series(age),
    #         'health': pd.Series(health),
    #         'absences': pd.Series(absences)
    #     })
    #     query = pd.get_dummies(query_df)
    #     prediction = clf.predict(query)
    #     return jsonify(np.ndarray(prediction).item())
    @app.route('/predict', methods=['POST'])
    def predict():
        if request.method == 'POST':
            json_data = request.get_json()
            df = pd.json_normalize(json_data)
            yesno_cols = ['paid','activities','nursery','higher','internet']
            df_num = df_num[df_num.columns.difference(yesno_cols)]
            df_yesno = pd.get_dummies(df[yesno_cols].astype(pd.CategoricalDtype(categories=['yes','no'])))
            df_processed = df_num.join(df_yesno)
            column_list = list(df_processed.columns) # change order
            df_processed = df_processed[column_list]
            result = model.predict(df_processed)[0]
            return jsonify({'prediction': result})


"""
curl -X 'POST' \
  '127.0.0.1:5000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
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
  "dalc": 5,
  "walc": 5,
  "health": 5,
  "absences": 93
}'
"""
