# Dependencies:
# libraries: sox curl postgresql
# python: wit flask flask-restful wikipedia owm psycopg2 googlemaps
from datetime import datetime, timedelta
import datetime as dt
import dateutil.parser
from dateutil.tz import *

import random

from flask import Flask, request
from flask_restful import Resource, Api

from jsonschema import validate

import wit_script

import weather

import wikipedia

import config

import psycopg2

continuation = None

def get_continuation():
    global continuation
    result = continuation
    continuation = None
    return result

def set_continuation(f):
    global continuation
    continuation = f

conn = psycopg2.connect(
    database=config.db_database,
    user=config.db_user,
    password=config.db_password,
    host=config.db_host
)

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
    loc = { 'lat': location['Latitude'], 'lot': location['Longitude'] }
    if 'location' in entities:
        loc = str(entities['location'][0]['value'])

    if 'datetime' in entities:
        date = dateutil.parser.parse(entities['datetime'][0]['value'])
        if entities['datetime'][0]['grain'] == 'day':
            date = date + timedelta(hours=12)
    else:
        date = datetime.now()

    continuation = ''
    if date.date() == dt.date(2015, 10, 05):
        continuation = " Don't forget to visit your mother."

    if 'weather_detail' in entities:
        filtered_detail = filter(lambda x: x['value'] in weather.possible_weather_detail, entities['weather_detail'])
        if len(filtered_detail) > 0:
            return weather.will_be_weather(loc, date, filtered_detail[0]['value']) + continuation

    return random.choice([weather.get_weather, weather.get_weather_verbose, weather.get_weather_very_verbose])(loc, date) + continuation

def handle_search(location, entities):
    search_term = entities['search_query'][0]['value']
    return wikipedia.summary(search_term, sentences=1)

def handle_navigate_places(location, entities):
    destination = entities['location'][0]['value']

    return 'Building path to ' + destination

def format_time(time, grain):
    now = datetime.now()

    # from pytz import reference
    # tz = reference.LocalTimezone()
    # time = time.astimezone(tz)

    result = ''
    if time.year != now.year:
        result += str(time.year) + ' year, '
    if time.year != now.year or time.month != now.month:
        result += time.strftime("%B") + ', '
    if time.year != now.year or time.month != now.month or time.day != now.day:
        result += str(time.day) + ', '
    result += time.strftime("%H:%M")

    return result

def handle_reminder(location, entities):
    time = None
    time_str = ''
    if 'datetime' in entities:
        time = dateutil.parser.parse(entities['datetime'][0]['value'])
        time_str = format_time(time, entities['datetime'][0]['grain'])

    action = None
    if 'reminder' in entities:
        action = entities['reminder'][0]['value']

    # TODO save in database

    return 'I will remind you to ' + action + ' at ' + time_str

intent_handlers = {
    'weather': handle_weather,
    'search': handle_search,
    'navigate_places': handle_navigate_places,
    'reminder': handle_reminder,
}

class Root(Resource):
    def post(self):
        args = request.get_json(force = True)
        validate(args, request_schema)
        
        continuation = get_continuation()
        if continuation is not None:
            return continuation(args)

        request_text = args['text']

        wit_response = wit_script.wit_function(config.wit_token, request_text)
        intent = wit_response['intent']

        if intent in intent_handlers:
            response_text = intent_handlers[intent](args['coordinates'], wit_response['entities'])
        else:
            response_text = "Can't handle intent " + intent

        # Generate questions and startListening?

        # Save request, response and location to database
        print 'Request: ', request_text
        print 'Response: ', response_text

        return { 'respText': response_text, 'startListening': False, 'intent': intent }

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
    weather.init_owm(config.pyowm_key)
    app.run(host = '0.0.0.0')
