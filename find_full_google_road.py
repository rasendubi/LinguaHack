import re
import json
import urllib
import requests
import googlemaps
from datetime import datetime 
from googlemaps import client as _client

def google_full_road_by_list(current_location, destination):
    googlemaps_key = 'AIzaSyCmNnoW_hRhHw9UgnOQKopVQrI2qnWy2pU'
    gmaps = googlemaps.Client(key=googlemaps_key)

    get_request = 'https://maps.googleapis.com/maps/api/directions/json?' + \
            urllib.urlencode({'origin': current_location, 'destination': destination, 'key': googlemaps_key})
    direct_http_result = requests.get(get_request)
    direct_http_result = direct_http_result.text

    json_direct_result = json.loads(direct_http_result)

    big_list = [s['legs'][0]['steps'] for s in json_direct_result['routes']][0]
    full_road = []
    for i in xrange(1, len(big_list)):
        full_road.append(big_list[i]['html_instructions'])

    return full_road

def google_full_road_by_string(current_location, destination):
    googlemaps_key = 'AIzaSyCmNnoW_hRhHw9UgnOQKopVQrI2qnWy2pU'
    gmaps = googlemaps.Client(key=googlemaps_key)

    get_request = 'https://maps.googleapis.com/maps/api/directions/json?' + \
            urllib.urlencode({'origin': current_location, 'destination': destination, 'key': googlemaps_key})
    direct_http_result = requests.get(get_request)
    direct_http_result = direct_http_result.text

    json_direct_result = json.loads(direct_http_result)

    big_list = [s['legs'][0]['steps'] for s in json_direct_result['routes']][0]

    full_road = ""
    for i in xrange(1, len(big_list)-1):
        full_road = full_road + unicode(big_list[i]['html_instructions']) + u", then "
    full_road = full_road + unicode(big_list[len(big_list)-1]['html_instructions'])

    full_road = tags_remove(full_road)

    return full_road

"""
Remove all tags which contains 
in every sublocatoin string
taked from direct json
"""
def tags_remove(raw_text):
    cleanr = re.compile('<.*?>')
    clean_text = re.sub(cleanr, '', raw_text)

    return clean_text

