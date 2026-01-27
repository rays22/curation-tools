#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Get pairs of partial matching strings from one list compared with another. """

__author__  = "Ray Stefancsik"
__version__ = "1.0"

#########################################################################
# Modules to import
#### Import command-line parsing module from the Python standard library.
#########################################################################
import argparse
import sys

### Mandatory positional arguments
parser = argparse.ArgumentParser( description='1. Take two sets of elements as lists. 2. Go through the elements in the first list and check if they partially match any elements in the second list. 3. Print the results to standard output.' )
parser.add_argument( 'your_list1', help='Path to your first list. FORMAT: Use a plain text file with one list element per line. Lines that start with # are ignored.' )
parser.add_argument( 'your_list2', help='Path to your second list file. FORMAT: Use a plain text file with one list element per line. Lines that start with # are ignored.' )

### Optional, but mutually exclusive user options:
group = parser.add_mutually_exclusive_group()
group.add_argument('-1', '--matching', help='Print the matching pairs only.', action='store_true')
group.add_argument('-2', '--no_match', help='Print the non-matching pairs only.', action='store_true')

######################################################################
# parse input data files
args = parser.parse_args()

# data input filenames

fname = args.your_list1
# Create an empty list for set 1
list1=list()

###############################
# parse the 1st input data file
###############################
# Create an empty list for set 1
list1=list()

# Check if the file exists before opening it.
fname = args.your_list1
try:
    fhand = open( fname )
except:
    print('File cannot be opened:', fname)
    exit()

# parse the data file
for line in fhand:
    if line.startswith('#'): # skip comments and header lines
        continue
    line = line.rstrip()
    list1.append(line)

# close file
fhand.close()

###############################
# parse the 2nd input data file
###############################
# Create an empty list for set 1
list2=list()

# Check if the file exists before opening it.
fname = args.your_list2
try:
    fhand = open( fname )
except:
    print('File cannot be opened:', fname)
    exit()

# parse the data file
for line in fhand:
    if line.startswith('#'): # skip header lines
        continue
    line = line.rstrip()
    list2.append(line)

# close file
fhand.close()


# initialise two empty lists to store the results
matching = []
no_match = []

for e2 in list2:
    for e1 in list1:
        if e1 in e2:
            matching.append((e1, e2))
        else:
            no_match.append((e1, e2))


# print the list of partially matching pairs

if args.matching:
    print("#### matching:")
    for i in matching:
        print(i)
    sys.exit() # stop here

# print the list of non-matching pairs

if args.matching:
    print("#### non-matching:")
    for i in no_match:
        print(i)
    sys.exit() # stop here

# print everything unless told otherwise if you get so far as this point

print("#### matching:")
for i in matching:
    print(i)

print("#### non-matching:")
for i in no_match:
    print(i)
