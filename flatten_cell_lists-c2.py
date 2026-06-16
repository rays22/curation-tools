#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Flatten cell lists of a table. """

__author__  = "Ray Stefancsik"
__version__ = "0.1"

######################################################################
# Import command-line parsing module from the Python standard library.
######################################################################
import argparse
import csv

# input filename
fname = 'filename?'

parser = argparse.ArgumentParser( description='Flatten a list from the second column in a table that share the first column, then print the first_column_value together with each of the desired list elements from the second column.', formatter_class=argparse.RawTextHelpFormatter )
### Positional arguments
parser.add_argument( 'input_file', help='Path to your input file.' )

### Optional arguments:
parser.add_argument('-c1', '--column_1', help='Header for column 1.', nargs='?', default='column_1', const='column_1') # if not specified by user then it defaults to given value
parser.add_argument('-c2', '--column_2', help='Header for column 2.', nargs='?', default='column_2', const='column_2') # if not specified by user then it defaults to given value
parser.add_argument('-f', '--filter', help='Filter values in column 2.', nargs='?', default=None, const=None) # if not specified by user then it defaults to given value
#parser.add_argument('-o', '--outfile', help='Path to output tsv file to (over)write.', nargs='?', default=None, const=None) # you need both the default and const for different scenarios (1. no flag and no user input, 2. flag only without any other user input, 3. flag plus user input. see https://docs.python.org/3/library/argparse.html
### Optional, but mutually exclusive user options:
group = parser.add_mutually_exclusive_group()
group.add_argument('-c', '--csv', help='Use comma as column separator.', action='store_true')
group.add_argument('-t', '--tab', help='Use tab as column separator.', action='store_true')

#################################################################

args = parser.parse_args()
# input filename
fname = args.input_file

### Input file format:
if args.csv:
    dlr = ',' #csv file format
else:
    dlr = '\t' #tsv file format

### get prefix string to be used as a filter for the second column
prefix = args.filter


#################################################################
# Read in a data file.
#################################################################

# try to open data file
try:
    fhand1 = open( fname )
except:
    print('File cannot be opened:', fname)
    exit()


with open(fname, mode="r", newline="", encoding="utf-8") as f:
        # Skip comment headers if they exist
        reader = csv.reader(f, delimiter=dlr)

        for row in reader:
            # Skip empty rows or header comment lines
            if not row or row[0].startswith("#"):
                continue

            cell1 = row[0]
            # Split the pipe-separated values in the second column
            cross_refs = row[1].split("|")

            for ref in cross_refs:
                if prefix == None:
                    print(f"{cell1}\t{ref}")
                else:
                    # Target only the values with a specified prefix
                    if ref.startswith(prefix):
                        print(f"{cell1}\t{ref}")


