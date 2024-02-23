# @name: hypothesis_api.py
# @creation_date: 2024-02-20
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Writes to the Hypothesis API 
# @acknowledgements:
# https://h.readthedocs.io/en/latest/api/
# https://pypi.org/project/hypothesis-api/

import hypothesis
import requests
import json
import re
from config import *

# VARIABLES

username=hypothesis_username
token=hypothesis_token
input_file=annotations_file

# SUBROUTINES

# function to perform text replacements in data
def data_replacements(data):
    data['url'] = re.sub('http:\/\/disruptivemedia\.org\.uk\/thepoliticalnatureofthebook\/', 'https://thepoliticalnatureofthebook.postdigitalcultures.org/', data['url'])
    
    if data['user'] != 'Janneke_Adema':
        data['text'] = 'Comment by ' + data['user'] + ': ' + data['text']
    return data

# function to set payload
def set_payload(data):

    h = hypothesis.Hypothesis(username=username, token=token)  # your h username and api token (from https://hypothes.is/account/developer)

    url = data['url']
    exact = data['exact']
    prefix = data['prefix']
    suffix = data['suffix']
    title = data['title']
    tags = data['tags']
    text = data['text']

    payload = {
        "uri": url,
        "target": 
            [{
                "source": [url],
                "selector": 
                    [{
                        "type": "TextQuoteSelector", 
                        "prefix": prefix,
                        "exact": exact,
                        "suffix": suffix
                        }
                    ]
            }], 
        "tags": tags,
        "text": text,
        "document": {
            "title": [title]
        },
        "permissions": h.permissions,
        "group": h.group
    }

    return payload

# function to write annotations to site
def write_annotations(payload):

    h = hypothesis.Hypothesis(username=username, token=token)  # your h username and api token (from https://hypothes.is/account/developer)

    r = h.post_annotation(payload)
    print(r.status_code)

# MAIN PROGRAM

with open(input_file) as json_file:
    data = json.load(json_file)
    a = 0
    for x in data[0]:
        if a >= 2: break
        x = data_replacements(x)
        payload = set_payload(x)
        #write_annotations(payload)
        print(payload)
        a += 1