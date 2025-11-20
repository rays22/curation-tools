#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Get the differences/agreements between lists/sets. You need to provide two plain text files that contain your desired lists in a format of one list element per line. """

__author__  = "Ray Stefancsik"
__version__ = "0.1"

#####COMMENT####### provide two lists to compute agreements or differences
#####COMMENT####my_list1 = [ "(likely gluten-specific) T FH CD4 T cells	CellType", "absorptive and secretory lineages	CellType", "absorptive lineages	CellType", "actively cycling ECs	CellType", "age-related B cells	CellType", "antigen-presenting cells	CellType", "APCs	CellType", "arterial	CellType", "B cell	CellType", "B cell lineages	CellType", "B cells	CellType", "BEST4 enterocytes	CellType", "branch 1 cells	CellType", "branch 2	CellType", "Brunner’s gland cells	CellType", "capillary	CellType", "CCL4	CellType", "CCL4 CD69 ITGAE population	CellType", "CCL4 cells	CellType", "CCL4 effector	CellType", "CCL4 effectors	CellType", "CCL4 populations	CellType", "CCR7 T FH -like subset	CellType", "CCR7 T FH CD4 T cells	CellType" ]
#####COMMENT####        
#####COMMENT####my_list2 = [ "ACD, CD8 T RM (2) cell	CellType", "age-related B cells	CellType", "B cell	CellType", "B cells	CellType", "BEST4 enterocytes	CellType", "Brunner’s gland cells	CellType", "CCL4 , IKZF2 T RM (2) and natural IEL populations	CellType", "CCL4 CD69 ITGAE	CellType", "CCL4 cells	CellType", "CCL4 effector and IKZF2 T RM (2) population	CellType", "CCR7 T FH -like	CellType", "CCR7 T FH CD4 T cells	CellType" ]
#####COMMENT####
#####COMMENT####my_set1 = set(my_list1)
#####COMMENT####my_set2 = set(my_list2)
#####COMMENT####
#####COMMENT##### find and print element found only in set 1
#####COMMENT####only_in_1 = list(my_set1 - my_set2) 
#####COMMENT####
#####COMMENT####print("\n\tonly in 1st:")
#####COMMENT####for i in only_in_1:
#####COMMENT####    print(i)
#####COMMENT####
#####COMMENT##### find and print element found only in set 2
#####COMMENT####only_in_2 = list(my_set2 - my_set1) 
#####COMMENT####
#####COMMENT####print("\n\tonly in 2nd:")
#####COMMENT####for i in only_in_2:
#####COMMENT####    print(i)
#####COMMENT####
#####COMMENT##### find and print common elements in two lists (intersection of two sets)
#####COMMENT######## find common elements in three lists: common_elements = my_set1.intersection(my_set2, my_set3)
#####COMMENT####
#####COMMENT####common_elements = my_set1.intersection(my_set2)
#####COMMENT####print("\n\tcommon elements:")
#####COMMENT####for i in list(common_elements):
#####COMMENT####    print(i)

#########################################################################
# Modules to import
#### Import command-line parsing module from the Python standard library.
#########################################################################
import argparse

### Mandatory positional arguments
parser = argparse.ArgumentParser( description='Look up items from a dictionary, convert them, and print the results to standard output.' )
parser.add_argument( 'your_list1', help='Path to your first data file. FORMAT: Use a plain text file with one list element per line. Lines that start with # are ignored.' )
parser.add_argument( 'your_list2', help='Path to your first data file. FORMAT: Use a plain text file with one list element per line. Lines that start with # are ignored.' )

### Optional, but mutually exclusive user options:
group = parser.add_mutually_exclusive_group()
group.add_argument('-1', '--only_in_1st', help='Get elements that are found only in the first set.', action='store_true')
group.add_argument('-2', '--only_in_2nd', help='Get elements that are found only in the second set.', action='store_true')
group.add_argument('-i', '--intersection', help='Get elements that are found in both sets.', action='store_true')

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

print("#### only in 1st:")
for i in only_in_1:
    print(i)

# find and print element found only in set 2
only_in_2 = set2 - set1

print("\n#### only in 2nd:")
for i in only_in_2:
    print(i)

# find and print common elements in two lists (intersection of two sets)
#### find common elements in three lists: common_elements = my_set1.intersection(my_set2, my_set3)

common_elements =set1.intersection(set2)
print("\n#### common elements:")
for i in list(common_elements):
    print(i)
