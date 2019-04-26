#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Look up items in a list from a dictionary. Results are printed to standard output. The user needs to provide a list in a file with one item per line. The dictionary to use must be also provided by the user in a two-column (tsv or csv) format."""

__author__  = "Ray Stefancsik"
__version__ = "2016-11-09"

# Modules to import
######################################################################
# Import command-line parsing module from the Python standard library.
######################################################################
import argparse

parser = argparse.ArgumentParser( description='Look up items from a dictionary, convert them, and print the results to standard output.' )
parser.add_argument( 'your_dictionary', help='Path to your dictionary file. FORMAT: Use two columns separated by tab (default) or comma (optional).' )
parser.add_argument( 'your_list', help='Path to your file with the list of items to convert using the dictionary. FORMAT: one item per line.' )

# Optional, but mutually exclusive user options:
group = parser.add_mutually_exclusive_group()
group.add_argument('-c', '--csv', help='Use comma as column separator.', action='store_true')
group.add_argument('-t', '--tab', help='Use tab as column separator.', action='store_true')


args = parser.parse_args()

######################################################################
# The dictionary to use must be provided by the user.
######################################################################

### Input file format:
if args.csv:
    delimiter = ',' #csv file format
else:
    delimiter = '\t' #tsv file format

# input filename
fname = args.your_dictionary


try:
    fhand = open( fname )
except:
    print('File cannot be opened:', fname)
    exit()

# Make an empty dictionary:
d = dict()

for line in fhand:
    line = line.rstrip()
    columns = line.split(delimiter)
    try:
        k = columns[0]
        v = columns[1]
    except:
        v = 'Check your dictionary file format.'
        print( 'ERROR:', v)
        exit()
    if k not in d:
        d[k] = v
# close file
fhand.close()

#################################################################
# Read in and convert data file.
#################################################################

fname = args.your_list

try:
    fhand = open( fname )
except:
    print('File cannot be opened:', fname)
    exit()

for line in fhand:
    words = line.rstrip()
    try:
        print(d[words])
    except:
        print( 'ERROR:', words ,'is not in your dictionary!!')
# close file
fhand.close()
