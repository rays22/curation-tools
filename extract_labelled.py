#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Extract and count unique labelled text spans from a label studio exported json file. """

__author__  = "Ray Stefancsik"
__version__ = "0.1"

######################################################################
# Import modules
######################################################################
import argparse # command-line parsing module from the Python standard library
import json # serialize, de-serialize, etc., JSON

######################################################################
# Obtain user input
######################################################################

### Mandatory positional arguments
parser = argparse.ArgumentParser( description='Extract and count unique labelled text spans from a label studio exported json file.', formatter_class=argparse.RawTextHelpFormatter )
parser.add_argument( 'input_file', help='path to your input file' )

### Optional arguments:
parser.add_argument('-p', '--pmcid', help='provide an identifier for yourdata file', nargs='?', default="use_filename_as_id", const="use_filename_as_id" ) # you need both the default and const for different scenarios (1. no flag and
# no user input, 2. flag only without any other user input, 3. flag plus user
# input. see https://docs.python.org/3/library/argparse.html

args = parser.parse_args()
# input filename
fname = args.input_file
pmcid = args.pmcid

if args.pmcid == "use_filename_as_id":
   pmcid  = fname

######################################################################
# Read in json data
######################################################################
with open(fname, mode="r", encoding="utf-8") as input_file:
    json_data = json.load(input_file)

######################################################################
# parse json data
######################################################################
# create an empty list for the results
results = []
# extract selected fields of interest
### strip whitespace from labelled text span
for i in json_data:
    for j in i["annotations"]:
        for k in j["result"]:
            for l in k["value"]["labels"]:
#               print(f'{pmcid}\t{l}\t"{k["value"]["text"]}"' ) # use double quote marks to surround text spans
                results.append('\t'.join([l, k["value"]["text"].strip()]))

# create an empty dictionary for counting unique text spans
counts = {}
# count unique label/text pairs 
for r in results:
    if r not in counts:
        counts[r] = 1
    else:
        counts[r] += 1

# test print unsorted counts:
#for key in counts:
#    print(f'{pmcid}\t{key}\t{counts[key]}')

# sort counts
sorted_counts = sorted(counts.items())

######################################################################
# print sorted results
######################################################################
# print headers
print(f'PUB_ID\tTEXT\tLABEL\tCOUNT')

# print sorted results as tab separated fields
for e in sorted_counts:
    print(f'{pmcid}\t{e[0]}\t{e[1]}')
