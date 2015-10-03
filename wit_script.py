import wit
import json

def wit_function(access_token, string):
    wit.init()
    response = json.loads(wit.text_query(string, access_token))
    wit.close()

    return response['outcomes'][0]
