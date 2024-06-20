# @name: hypothesis_api.py
# @creation_date: 2024-02-20
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Performs various functions against the Hypothesis API 
# @acknowledgements:
# https://h.readthedocs.io/en/latest/api/
# https://pypi.org/project/hypothesis-api/
# https://github.com/hypothesis/batch-tools/blob/main/batch_tools/bulk_delete.py

import hypothesis
import requests
import json
import pprint
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

# function to process user string to remove extraneous text
def process_user(data):
    data['user'] = data['user'][5:][:-12]
    return data

# function to replace ref IDs with new IDs
def replace_refs(data, ids):
    for i, item in enumerate(data['refs']):
        if item in ids:
            data['refs'][i] = ids[item]
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

# function to write annotation to site
def write_annotation(payload):

    h = hypothesis.Hypothesis(username=hypothesis_username, token=hypothesis_token)  # your h username and api token (from https://hypothes.is/account/developer)

    r = h.post_annotation(payload)

    response_text = json.loads(r.text)

    print(r.status_code)

    return (response_text['id'])

# function to import single annotation
def import_annotation(annotation):

    annotation = replace_url(annotation)
    # subroutine to add the original user's name in the body of the annotation
    annotation = add_user(annotation)
    payload = set_payload(annotation)
    new_id = write_annotation(payload)

    return(new_id)

# function to import a single reply annotation to site
def import_reply(annotation, ids):
    annotation = replace_url(annotation)
    # subroutine to add the original user's name in the body of the annotation
    annotation = add_user(annotation)
    # subroutine to replace the ref IDs from the original file with the newly imported annotation IDs
    annotation = replace_refs(annotation, ids)
    payload = set_payload(annotation)
    new_id = write_annotation(payload)

    return(new_id)

# function to import annotations to site
def import_annotations():

    with open(annotations_file) as json_file:
        data = json.load(json_file)
        # sort by date created
        data[0].sort(key=lambda x: x['created'])
        # sort by start point (if there is one)
        data[0].sort(key=lambda x: x.get('start', float('inf')))
        a = 0
        ids = {}
        for x in data[0]:
            # import annotations that aren't replies i.e. that do not have 'refs' to other annotations
            if not x['refs']:
                #if a >= 2: break
                new_id = import_annotation(x)
                #a += 1
            # import annotations that are replies i.e. that do have 'refs' to other annotations
            else:
                new_id = import_reply(x, ids)
            
            ids[x['id']] = new_id
                
# function to export annotations from old_url site
def export_annotations():

    h = hypothesis.Hypothesis(username=hypothesis_username, token=hypothesis_token)  # your h username and api token (from https://hypothes.is/account/developer)

    search_parameters = {
        "wildcard_uri": old_url + '*',
        "limit": '200'
    }

    search_results = h.search(params=search_parameters)

    if search_results['total'] == 0:
        print("no annotations found")
        sys.exit(0)

    else: 
        with open('data.json', 'w') as f:
            for record in search_results['rows']:
                process_user(record)
            json.dump(search_results['rows'], f, indent=2)

# function to delete annotations from new_url site
def delete_annotations():

    h = hypothesis.Hypothesis(username=hypothesis_username, token=hypothesis_token)  # your h username and api token (from https://hypothes.is/account/developer)

    search_parameters = {
        "wildcard_uri": new_url + '*',
        "limit": '200'
    }

    search_results = h.search(params=search_parameters)

    if search_results['total'] == 0:
        print("no annotations found")
        sys.exit(0)

    else: 
        print(f"found {search_results['total']} matching annotations. are you sure you want to delete these? type 'yes' or 'no'.")
        ok = input()

        if ok.lower() not in ["y", "yes", "1", "true"]:
            print("deletion cancelled")
            sys.exit(0)

        else:
            for x in search_results['rows']:
                h.delete_annotation(x['id'])

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
    elif sys.argv[1] == 'export':
        export_annotations()
    elif sys.argv[1] == 'delete':
        delete_annotations()
    else:
        get_help()