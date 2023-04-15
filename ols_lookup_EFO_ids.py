#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Look up ontology labels and definitions based on CURIEs identifiers using the EMBL-EBI OLS REST API. """

__author__  = "Ray Stefancsik"
__version__ = "0.1"

######################################################################
######################################################################
import requests # to make API requests
import argparse # to take CLI user input

# function definition from https://hackersandslackers.com/extract-data-from-complex-json-python/
def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

######################################################################
### Read in file with a list of CURIEs.
# input filename
fname = 'filename?'

parser = argparse.ArgumentParser( description='Proved a list of compact uniform resource identifiers (CURIEs, e.g. EFO:0005273) in a text file in a format of one CURIE per line.', formatter_class=argparse.RawTextHelpFormatter )

### Mandatory positional argument
parser.add_argument( 'input_file', help='Path to your input file.' )

### Optional, but mutually exclusive user option:
group = parser.add_mutually_exclusive_group()
group.add_argument('-d', '--definition', help='Look up term definition.', action='store_true')

args = parser.parse_args()
# input filename
fname = args.input_file

# Use the OLS 4 endpoint to retrieve terms only from defining ontology 
## see OLS 3 documentation at https://www.ebi.ac.uk/ols/docs/api 
### for example
### http://www.ebi.ac.uk/ols/api/terms/findByIdAndIsDefiningOntology?iri=http://www.ebi.ac.uk/efo/EFO_0005273
### https://www.ebi.ac.uk/ols4/api/terms/findByIdAndIsDefiningOntology?iri=http://www.ebi.ac.uk/efo/EFO_0005273
### http://www.ebi.ac.uk/ols/api/terms/findByIdAndIsDefiningOntology?id=EFO:0000001

# API endpoint to use
BASE_OLS_URL = f'https://www.ebi.ac.uk/ols4/api/terms/findByIdAndIsDefiningOntology?iri='

#################################################################
# print header line
if args.definition:
    print("CURIE\tLabel\tDefinition")
else:
    print("CURIE\tLabel")

#################################################################
# Attempt to read in a data file.
#################################################################
try:
    fhand1 = open( fname )
except:
    print('File cannot be opened:', fname)
    exit()

# read in data
for line in fhand1:
    if line.startswith('#'): # skip header line
        continue
    line = line.rstrip() # strip whitespace
    curie = line
    columns = line.split(':')
    prefix = columns[0]
    # You need to convert the compact uniform resource identifiers (CURIEs) to EBI PURLs (e.g. EFO:0005273 --> http://www.ebi.ac.uk/efo/EFO_0005273, 
    # or OBO Library PURLs, e.g. OBA:VT0002460 --> http://purl.obolibrary.org/obo/OBA_VT0002460
    if prefix.lower() == 'efo':
        IRI_BASE = 'http://www.ebi.ac.uk/efo/'
    else:
        IRI_BASE = 'http://purl.obolibrary.org/obo/'
    purl = BASE_OLS_URL + IRI_BASE + curie.replace(':', '_')
    #print(purl) # for debugging
    response = requests.get(purl).json()
    if json_extract(response, 'label'):
        label = json_extract(response, 'label')
        if args.definition:
            if response['_embedded']['terms'][0]['description'][0]:
                description = response['_embedded']['terms'][0]['description'][0]
            else:
                description = 'N/A'
        else:
            description = ''
        print(f"{curie}\t{label[0]}\t{description}")
    else:
        label = 'N/A'
        print(f"{curie}\t{label[0]}\t")

# close file
fhand1.close()
