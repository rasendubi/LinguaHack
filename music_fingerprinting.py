import json
import sys
import os
import base64
import hmac
import hashlib
import time
import requests  

access_key = ""
access_secret = ""

requrl = "http://ap-southeast-1.api.acrcloud.com/v1/identify"
http_method = "POST"
http_uri = "/v1/identify"
data_type = "audio"
signature_version = "1"
timestamp = time.time()

string_to_sign = http_method+"\n"+http_uri+"\n"+access_key+"\n"+data_type+"\n"+signature_version+"\n"+str(timestamp)

sign = base64.b64encode(hmac.new(access_secret, string_to_sign, digestmod=hashlib.sha1).digest())

f = open(sys.argv[1], "rb")
sample_bytes = os.path.getsize(sys.argv[1])

files = {'sample':f}
data = {'access_key':access_key,
        'sample_bytes':sample_bytes,
        'timestamp':str(timestamp),
        'signature':sign,
        'data_type':data_type,
        "signature_version":signature_version}

r = requests.post(requrl, files=files, data=data)
r.encoding = "utf-8"

read_response = json.loads(r.text)

artist = read_response["metadata"]["music"][0]["artists"][0]["name"]
song = read_response["metadata"]["music"][0]["title"]

print "Artist:", artist
print "Song:", song

