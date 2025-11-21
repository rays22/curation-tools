#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Get the differences/agreements between lists/sets. You need to provide two plain text files that contain your desired lists in a format of one list element per line. """

__author__  = "Ray Stefancsik"
__version__ = "1.0"

#########################################################################
# Modules to import
#### Import command-line parsing module from the Python standard library.
#########################################################################
import argparse
import sys

### Mandatory positional arguments
parser = argparse.ArgumentParser( description='1. Take two sets of elements as lists. 2. Find the shared and non-shared elements in the two sets. 3. Print the results to standard output.' )
parser.add_argument( 'your_list1', help='Path to your first data file. FORMAT: Use a plain text file with one list element per line. Lines that start with # are ignored.' )
parser.add_argument( 'your_list2', help='Path to your first data file. FORMAT: Use a plain text file with one list element per line. Lines that start with # are ignored.' )

### Optional, but mutually exclusive user options:
group = parser.add_mutually_exclusive_group()
group.add_argument('-1', '--only_in_1st', help='Get the elements that are found only in the first set.', action='store_true')
group.add_argument('-2', '--only_in_2nd', help='Get the elements that are found only in the second set.', action='store_true')
group.add_argument('-i', '--intersection', help='Get the elements that are found in both sets.', action='store_true')

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
    if line.startswith('#'): # skip header lines
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

###############################
# convert input lists to sets
set1 = set(list1)
set2 = set(list2)

###############################

# find and print element found only in set 1
only_in_1 = set1 - set2
only_in_1 = sorted(only_in_1) # sort iterables


if args.only_in_1st:
    print("#### only in 1st:")
    for i in only_in_1:
        print(i)
    sys.exit() # stop here

# find and print element found only in set 2
only_in_2 = set2 - set1
only_in_2 = sorted(only_in_2) # sort iterables

if args.only_in_2nd:
    print("#### only in 2nd:")
    for i in only_in_2:
        print(i)
    sys.exit() # stop here

# find and print common elements in two lists (intersection of two sets)
#### find common elements in three lists: common_elements = my_set1.intersection(my_set2, my_set3)

common_elements = set1.intersection(set2)
common_elements = sorted(common_elements)

if args.intersection:
    print("#### common elements:")
    for i in list(common_elements):
        print(i)
    sys.exit() # stop here

#  print default output if not otherwise told

print("#### only in 1st:")
for i in only_in_1:
    print(i)
print("\n#### only in 2nd:")
for i in only_in_2:
    print(i)
print("\n#### common elements:")
for i in list(common_elements):
    print(i)
