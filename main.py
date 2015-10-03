# Dependencies:
# libraries: sox, curl
# python: wit flask flask-restful wikipedia owm
from datetime import datetime

from flask import Flask, request
from flask_restful import Resource, Api

from jsonschema import validate

import wit_script

import weather

import wikipedia

import config

mock_token = 'jaskldfjaslkdf'

request_schema = {
    'type': 'object',
    'properties': {
        'text': {'type': 'string'},
        'coordinates': {
            'type': 'object',
            'properties': {
                'Latitude': { 'type': 'number' },
                'Longitude': { 'type': 'number' }
            },
            'required': ['Latitude', 'Longitude']
        }
    },
    'required': ['text']
}

auth_schema = {
    'type': 'object',
    'properties': {
        'user': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['user', 'password']
}

app = Flask(__name__)
app.debug = True

api = Api(app)

def handle_weather(location, entities):
    location = 'London, UK'
    date = datetime.now()
    print date
    return weather.get_weather(config.pyowm_key, location, date)

def handle_search(location, entities):
    search_term = entities['search_query'][0]['value']
    return wikipedia.summary(search_term, sentences=1)

intent_handlers = {
    'weather': handle_weather,
    'search': handle_search
}

class Root(Resource):
    def post(self):
        args = request.get_json(force = True)
        validate(args, request_schema)
        
        request_text = args['text']

        wit_response = wit_script.wit_function(config.wit_token, request_text)
        intent = wit_response['intent']

        if intent in intent_handlers:
            response_text = intent_handlers[intent](args['coordinates'], wit_response['entities'])
        else:
            response_text = "Can't handle intent " + intent

        # Generate questions and startListening?

        # Save request, response and location to database

        return { 'respText': response_text, 'startListening': False }

class Authorize(Resource):
    def post(self):
        args = request.get_json(force = True)
        validate(args, auth_schema)

        if args['user'] == 'test' and args['password'] == 'testpass':
            return { 'result': 'ok', 'token': mock_token }

        return { 'result': 'error text' }

api.add_resource(Root, '/')
api.add_resource(Authorize, '/auth')

if __name__ == '__main__':
    app.run(host = '0.0.0.0')
