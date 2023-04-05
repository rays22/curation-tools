#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" This CLI called jaccard
    - takes as an input a text file with a list of disease identifiers (found in resources/diseases.txt)
   - accesses the BioLink API (https://api.monarchinitiative.org/api/) to obtain all phenotypes associated with each disease in that list
   - computes a pairwise Jaccard score between all diseases (even if you do not know what a Jaccard score is right now, you should be able to find out)
   - Writes an output TSV file with three columns: `disease_1`, `disease_2`, `jaccard` (see example below) for each unique disease pair (if you include MONDO:0007947 | MONDO:0013426, you should _not_ include MONDO:0013426 | MONDO:0007947). """

__author__  = "Ray Stefancsik"
__version__ = "0.1"

######################################################################
# This is needed to make API requests
import requests
# This is to help work with JSON.
import json
# Import command-line parsing module from the Python standard library.
import argparse
# To help produce tsv output
import csv
######################################################################

# input filename
fname = 'filename?'

parser = argparse.ArgumentParser( description='Provide a text file with a list of MONDO disease identifiers. Format: one identifier per line.', formatter_class=argparse.RawTextHelpFormatter )

### Mandatory positional argument
parser.add_argument( 'input_file', help='Path to your input file.' )

### Optional arguments:
parser.add_argument('-o', '--outfile', help='Path to your desired output tsv file to be (over)written.', nargs='?', default=None, const=None) # you need both the default and const for different scenarios (1. no flag and no user input, 2. flag only without any other user input, 3. flag plus user input. see https://docs.python.org/3/library/argparse.html

### Optional, but mutually exclusive user option:
group = parser.add_mutually_exclusive_group()
group.add_argument('-s', '--sort_results', help='Sort results by descending Jaccard score.', action='store_true')

args = parser.parse_args()
# input filename
fname = args.input_file

#################################################################
# Read in a data file.
#################################################################

try:
    fhand1 = open( fname )
except:
    print('File cannot be opened:', fname)
    exit()
disease_ids = []
for line in fhand1:
    if line.startswith('#'): # skip comments
        continue
    line = line.strip() # strip white-space
## populate the dictionary with gene symbol values:
    disease_ids.append(line)
# close file
fhand1.close()

# Get the set of unique disease pairs
disease_pairs = [(disease_ids[i], disease_ids[j]) for i in range(len(disease_ids)) for j in range(i+1, len(disease_ids))]

def jaccard (disease1, disease2):
    """ Accesses the BioLink API (https://api.monarchinitiative.org/api/) to obtain a pairwise Jaccard score"""

    # Get pairwise similarity example
    # https://api.monarchinitiative.org/api/pair/sim/jaccard/{id1}/{id2}
    # https://api.monarchinitiative.org/api/pair/sim/jaccard/MONDO%3A0007947/MONDO%3A0013426
    BIOLINK_API_JACQUARD_URL = "https://api.monarchinitiative.org/api/pair/sim/jaccard/"
    BIOLINK_API_JACQUARD_QUERY_URL = BIOLINK_API_JACQUARD_URL + requests.utils.quote(disease1 + "/" + disease2)
    response = requests.get(BIOLINK_API_JACQUARD_QUERY_URL)
    return(response.text)

# compute results
results = [ ['disease_1', 'disease_2', 'jaccard'] ]
for i in disease_pairs:
    similarity = jaccard(i[0], i[1])
    results.append([i[0], i[1], similarity.strip()])

# sort results by descending Jaccard score
if args.sort_results:
    results.sort(key = lambda x: x[2], reverse = True)
#else:
#    print("Not sorting.")

if args.outfile == None:
    for r in results:
        print(*r) # using the '*' or 'splat' operator
else:
    print("For the results, check the file:", args.outfile)
    with open(args.outfile, 'w', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
        for record in results:
            writer.writerow( record )
