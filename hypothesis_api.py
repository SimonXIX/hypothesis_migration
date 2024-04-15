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
import sys

# SUBROUTINES

# function to fetch help text
def get_help():
    f = open('help.md', 'r')
    help_text = f.read()
    print(help_text)

# function to fetch license text
def get_license():
    f = open('LICENSE', 'r')
    license_text = f.read()
    print(license_text)

# function to perform URL replacement
def replace_url(data):
    data['url'] = re.sub(old_url, new_url, data['url'])
    if "index1.html" in data['url']:
        data['url'] = new_url
    return data

# function to add the original user's name in the body of the annotation
def add_user(data):
    if data['user'] != 'Janneke_Adema':
        data['text'] = 'Comment by ' + data['user'] + ': ' + data['text']
    return data

# function to set payload
def set_payload(data):

    h = hypothesis.Hypothesis(username=hypothesis_username, token=hypothesis_token)  # your h username and api token (from https://hypothes.is/account/developer)

    url = data['url']
    exact = data['exact']
    prefix = data['prefix']
    suffix = data['suffix']
    title = data['title']
    tags = data['tags']
    text = data['text']
    refs = data['refs']

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
        "group": h.group,
        "references": refs
    }

    return payload

# function to write annotations to site
def write_annotations(payload):

    h = hypothesis.Hypothesis(username=hypothesis_username, token=hypothesis_token)  # your h username and api token (from https://hypothes.is/account/developer)

    r = h.post_annotation(payload)
    print(r.status_code)

# function to import annotations to site
def import_annotations():
    with open(annotations_file) as json_file:
            data = json.load(json_file)
            a = 0
            for x in data[0]:
                #if a >= 1: break
                x = replace_url(x)
                # subroutine to add the original user's name in the body of the annotation
                x = add_user(x)
                payload = set_payload(x)
                #write_annotations(payload)
                print(payload)
                #a += 1

# MAIN PROGRAM

if len(sys.argv) == 1:
    get_help()
else:
    if sys.argv[1] == 'help':
        get_help()
    elif sys.argv[1] == 'license':
        get_license()
    elif sys.argv[1] == 'import':
        import_annotations()
    else:
        get_help()