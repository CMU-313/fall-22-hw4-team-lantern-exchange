import json
from flask import Flask
import pytest


from app.handlers.routes import configure_routes

# test if the root url shows the correct information
def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data() == b'try the predict route it is great!'

# test if a correct POST request succeeds
def test_predict_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
    jsonInput = {
        "school": "GP", "traveltime": 2, "studytime": 2, 
        "failures": 0, "paid": "yes", "activities": "yes", 
        "nursery": "yes", "higher": "yes", "internet": "yes",
        "freetime": 3, "goout": 2, "Dalc": 1, "Walc": 1,
        "health": 5, "absences": 0
    }
    response = client.post(url, json=jsonInput)
    assert response.status_code == 200

# test if response type if correct
def test_predict_route_content():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
    jsonInput = {
        "school": "GP", "traveltime": 2, "studytime": 2, 
        "failures": 0, "paid": "yes", "activities": "yes", 
        "nursery": "yes", "higher": "yes", "internet": "yes",
        "freetime": 3, "goout": 2, "Dalc": 1, "Walc": 1,
        "health": 5, "absences": 0
    }
    response = client.post(url, json=jsonInput)
    assert response.status_code == 200
    assert response.content_type == "application/json"

# test bad input 1: input fields do not match
def test_predict_route_bad_input_1(): 
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
    jsonInput = {
        "pstatus": "A", "medu": 0, "fedu": 0, "mjob": "1", "fjob": "1", 
        "reason": "other", "guardian": "mother", "traveltime": 0, "studytime": 2, 
        "failures": 4, "schoolsup": "no", "famsup": "no", "paid": "no", 
        "activities": "yes", "nursery": "no", "higher": "no", "internet": "yes",
        "romantic": "no", "famrel": 3, "freetime": 5, "goout": 5, 
        "dalc": 3, "walc": 5, "health": 3, "absences": 4}
    
    response = client.post('/predict', json=jsonInput)
    assert response.status_code != 200

# test bad input 2: "CMU" is not one of "GP" and "MS"
def test_predict_route_bad_input_2(): 
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
    jsonInput = {
        "school": "CMU", "traveltime": 2, "studytime": 2, 
        "failures": 0, "paid": "yes", "activities": "yes", 
        "nursery": "yes", "higher": "yes", "internet": "yes",
        "freetime": 3, "goout": 2, "Dalc": 1, "Walc": 1,
        "health": 5, "absences": 0
    }
    response = client.post('/predict', json=jsonInput)
    assert response.status_code != 200 

# test bad input 3: higher is not one of "yes" and "no"
def test_predict_route_bad_input_3(): 
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
    jsonInput = {
        "school": "MS", "traveltime": 2, "studytime": 2, 
        "failures": 0, "paid": "yes", "activities": "yes", 
        "nursery": "yes", "higher": "yeah", "internet": "yes",
        "freetime": 3, "goout": 2, "Dalc": 1, "Walc": 1,
        "health": 5, "absences": 0
    }
    response = client.post('/predict', json=jsonInput)
    assert response.status_code != 200

# test bad input 4: The number of absences exceeds 
# the largest possible number
def test_predict_route_bad_input_4(): 
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
    jsonInput = {
        "school": "MS", "traveltime": 2, "studytime": 2, 
        "failures": 0, "paid": "yes", "activities": "yes", 
        "nursery": "yes", "higher": "yeah", "internet": "yes",
        "freetime": 3, "goout": 2, "dalc": 1, "Walc": 1,
        "health": 5, "absences": 94
    }
    response = client.post('/predict', json=jsonInput)
    assert response.status_code != 200 

# test bad input 5: missing required input field 
# ("Dalc" is required by "dalc" is given)
def test_predict_route_bad_input_5(): 
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
    jsonInput = {
        "school": "MS", "traveltime": 2, "studytime": 2, 
        "failures": 0, "paid": "yes", "activities": "yes", 
        "nursery": "yes", "higher": "yeah", "internet": "yes",
        "freetime": 3, "goout": 2, "dalc": 1, "Walc": 1,
        "health": 5, "absences": 0
    }
    response = client.post('/predict', json=jsonInput)
    assert response.status_code != 200 


# test if responses are 0 or 1 in the correct json format
def test_predict_route_response_edge_case(): 
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
    jsonInput = {
        "school": "GP", "traveltime": 2, "studytime": 2, 
        "failures": 0, "paid": "yes", "activities": "yes", 
        "nursery": "yes", "higher": "yes", "internet": "yes",
        "freetime": 3, "goout": 2, "Dalc": 1, "Walc": 1,
        "health": 5, "absences": 0
    }
    expectedResponse_0 = {
        "prediction": 0, 
    }
    expectedResponse_1 = {
        "prediction": 1, 
    }
    response = client.post('/predict', json=jsonInput)
    assert response.status_code == 200 
    assert json.loads(response.data) == expectedResponse_0 \
        or json.loads(response.data) == expectedResponse_1

# test for requests that do not have a request body
def test_predict_route_missing_request_body(): 
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
    response = client.post('/predict')
    assert response.status_code != 200 

# test receiving get requests when we only support post requests
def test_predict_route_wrong_get_request(): 
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'
    jsonInput = {
        "school": "GP", "traveltime": 2, "studytime": 2, 
        "failures": 0, "paid": "yes", "activities": "yes", 
        "nursery": "yes", "higher": "yes", "internet": "yes",
        "freetime": 3, "goout": 2, "Dalc": 1, "Walc": 1,
        "health": 5, "absences": 0
    }
    response = client.get(url, json=jsonInput)
    assert response.status_code != 200 
