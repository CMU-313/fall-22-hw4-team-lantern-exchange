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
    app = Flask(__name__)
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
    jsonInput = {"age": 0, "address": "",
                "pstatus": "", "medu": 0, "fedu": 0, "mjob": "", "fjob": "", 
                "reason": "", "traveltime": 0, "studytime": 0, 
                "failures": 0, "schoolsup": "", "famsup": "", "paid": "", 
                "activities": "", "nursery": "", "higher": "", "internet": "",
                "romantic": "", "famrel": 0, "freetime": 0, "goout": 0, 
                "dalc": 0, "walc": 0, "health": 0, "absences": 0}
    response = client.post(url, json=jsonInput)
    assert response.status_code == 200
        
def test_predict_bad_student_route(): 
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
    jsonInput =  {"pstatus": "A", "medu": 0, "fedu": 0, "mjob": "1", "fjob": "1", 
                "reason": "other", "guardian": "mother", "traveltime": 0, "studytime": 2, 
                "failures": 4, "schoolsup": "no", "famsup": "no", "paid": "no", 
                "activities": "yes", "nursery": "no", "higher": "no", "internet": "yes",
                "romantic": "no", "famrel": 3, "freetime": 5, "goout": 5, 
                "dalc": 3, "walc": 5, "health": 3, "absences": 4}
    
    response = client.post('/predict', json=jsonInput)
    assert response.status_code != 200 
    
#edge case, with no responses
def test_predict_edge_case(): 
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
    jsonInput =  {"age": 0, "address": "", "famsize": "", 
            "pstatus": "", "medu": 0, "fedu": 0, "mjob": "", "fjob": "", 
            "reason": "", "traveltime": 0, "studytime": 0, 
            "failures": 0, "schoolsup": "", "famsup": "", "paid": "", 
            "activities": "", "nursery": "", "higher": "", "internet": "",
            "romantic": "", "famrel": 0, "freetime": 0, "goout": 0, 
            "dalc":0, "walc": 0, "health": 0, "absences":0}
    expectedResponse = {
        "student G3": 0, 
    }
    
    response = client.get('/predict')
    assert response.status_code == 200 
    assert json.loads(response.data) == expectedResponse
