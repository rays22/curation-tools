#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Replace some lines in a text stream using a dictionary."""

__author__  = "Ray Stefancsik"
__version__ = "2022-05-16."

# Modules to import
######################################################################
# Import command-line parsing module from the Python standard library.
######################################################################
import argparse

### Mandatory positional arguments
parser = argparse.ArgumentParser( description='Replace some lines in a text stream from a file. DESCRIPTION: This command line tool reads the lines from a plain text file, strips any surrounding white space and tries to look up the line as a string from a dictionary. It then converts the matching line and prints it (or prints the non-matching line unchanged) to standard output.' )
parser.add_argument( 'your_dictionary', help='Path to your dictionary file. FORMAT: Use two columns separated by tab (default) or comma (optional).' )
parser.add_argument( 'your_list', help='Path to your text file with the lines to be replace based on your provided dictionary.' )

### Optional, but mutually exclusive user options:
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

with open(fname, "r") as file:
    readline = file.read().split("\n") # remove any explicit new line characters
    for line in readline:
        try:
            print(d[line])
        except:
            print(line)

# close file
fhand.close()
