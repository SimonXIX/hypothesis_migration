# Python script to migrate Hypothes.is annotations

While migrating some legacy websites from one server to another, I came across the problem of moving Hypothes.is annotations from one website to another. There is no automated way to migrate within Hypothes.is and there has been an open issue with Hypothes.is since 2017 to allow users to inform them about 3xx redirects for URLs (https://github.com/hypothesis/product-backlog/issues/203). Since this was an open issue, I wrote my own script. 

## exporting annotations

You can migrate annotations from the old site using Jon Udell's export tool available at https://jonudell.info/h/facet/. This can view annotations from a given URL or wildcard URI. You can then save the annotations as HTML, CSV, or Json. This script uses Json. 

## configuration variables

Start by copying config_template.py to a file called config.py. Fill in the configuration variables using your own details. 

hypothesis_username and hypothesis_token can be obtained following Hypothes.is' own API documentation at https://h.readthedocs.io/en/latest/api/authorization/. 

>By generating a personal API token on the [Hypothesis developer page](https://hypothes.is/account/developer) (you must be logged in to Hypothesis to get to this page). This is the simplest method, however these tokens are only suitable for enabling your application to make requests as a single specific user.

annotations_file should be the Json file exported using Jon Udell's export tool. 

old_url should be the old base URL for the site exported from. 

new_url should be the new base URL. 

## running the script

Ensure that you have all the required Python modules by running:

`pip install -r requirements.txt`

The script has several functions which can be run by changing the parameter in the command:

`python3 hypothesis_api.py [license|help|import|delete]`

'license' prints the MIT License.

'help' prints a simple help file (saved here as help.md).

'import' runs the main import process. This will import all the annotations in file pointed too by the annotations_file config variable including top-level annotations and replies underneath those annotations.

'export' runs an export of all annotations from old_url to a file called data.json.

'delete' will run a bulk deletion process on all annotations at the new_url config variable website.