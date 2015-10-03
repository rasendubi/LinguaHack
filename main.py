from flask import Flask, request
from flask_restful import Resource, Api

from jsonschema import validate

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

class Root(Resource):
    def post(self):
        args = request.get_json(force = True)
        validate(args, request_schema)
        
        request_text = args['text']

        # Parse request_string with wit.ai

        # Dispatch request

        # Generate questions and startListening?

        # Save request, response and location to database

        return { 'respText': request_text, 'startListening': False }

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
