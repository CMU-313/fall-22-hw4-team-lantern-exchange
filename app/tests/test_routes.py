import json
from flask import Flask
import pytest


from app.handlers.routes import configure_routes


def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data() == b'try the predict route it is great!'

def test_predict_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
    jsonInput = {"school": "", "sex": "", "age": 0, "address": "", "famsize": "", 
                "pstatus": "", "medu": 0, "fedu": 0, "mjob": "", "fjob": "", 
                "reason": "", "guardian": "", "traveltime": 0, "studytime": 0, 
                "failures": 0, "schoolsup": "", "famsup": "", "paid": "", 
                "activities": "", "nursery": "", "higher": "", "internet": "",
                "romantic": "", "famrel": 0, "freetime": 0, "goout": 0, 
                "dalc": 0, "walc": 0, "health": 0, "absences": 0}
    response = client.post(url, json=jsonInput)
    assert response.status_code == 200
