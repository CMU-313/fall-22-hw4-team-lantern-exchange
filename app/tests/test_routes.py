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
 


#tests if content received is in json format
def test_base_content(): 
    app = Flash(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'
    
    response = client.get('/')
    assert response.status_code == 200
    assert response.content_type == "application/json"

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
    
def test_predict_great_student_route(): 
    jsonInput =  {"school": "", "sex": "", "age": 22, "address": "U", "famsize": "", 
                "pstatus": "T", "medu": 0, "fedu": 0, "mjob": "4", "fjob": "4", 
                "reason": "other", "guardian": "mother", "traveltime": 0, "studytime": 4, 
                "failures": 1, "schoolsup": "yes", "famsup": "yes", "paid": "yes", 
                "activities": "yes", "nursery": "yes", "higher": "yes", "internet": "yes",
                "romantic": "no", "famrel": 5, "freetime": 5, "goout": 5, 
                "dalc": 1, "walc": 1, "health": 5, "absences": 1}
    expectedResponse = {
        "student G3": 18, 
        "probabilities": {
            15: 0.1
            20: 0.4, 
            18: 0.5
        }
    }
    
    response = client.get('/predict')
    assert response.status_code == 200 
    assert json.loads(response.data) == expectedResponse
    
def test_predict_bad_student_route(): 
    jsonInput =  {"school": "", "sex": "", "age": 22, "address": "R", "famsize": "5", 
                "pstatus": "A", "medu": 0, "fedu": 0, "mjob": "1", "fjob": "1", 
                "reason": "other", "guardian": "mother", "traveltime": 0, "studytime": 2, 
                "failures": 4, "schoolsup": "no", "famsup": "no", "paid": "no", 
                "activities": "yes", "nursery": "no", "higher": "no", "internet": "yes",
                "romantic": "no", "famrel": 3, "freetime": 5, "goout": 5, 
                "dalc": 3, "walc": 5, "health": 3, "absences": 4}
    expectedResponse = {
        "student G3": 7, 
        "probabilities": {
            10: 0.1
            12: 0.4, 
            7: 0.5
        }
    }
    
    response = client.get('/predict')
    assert response.status_code == 200 
    assert json.loads(response.data) == expectedResponse
