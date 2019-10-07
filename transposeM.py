#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Transpose a matrix. Convert columns going from left to right to rows going from top to bottom in such a way that column headers (i.e. the first row of the original matrix) shall be the first column in the transposed matrix.  The input file must be in tab- or comma-separated values (csv or tsv) format."""

__author__  = "Ray Stefancsik"
__version__ = "01"

######################################################################
# Import command-line parsing module from the Python standard library.
######################################################################
import argparse

# assign initial value for input filename
fname = 'filename?'

parser = argparse.ArgumentParser( description='Transpose matrix. Convert columns going from left to right to rows going from top to bottom and print the results to standard output.', formatter_class=argparse.RawTextHelpFormatter )
parser.add_argument( 'input_file', help='Path to your input file.' )

# Optional, but mutually exclusive user options:
group = parser.add_mutually_exclusive_group()
group.add_argument('-t', '--tab', help='Use tab as column separator (default).', action='store_true')
group.add_argument('-c', '--csv', help='Use comma as column separator.', action='store_true')

args = parser.parse_args()
#################################################################
# Read in a data file.
#################################################################
# input filename
fname = args.input_file
### Input file format:
if args.csv:
    delimiter = ',' #csv file format
else:
    delimiter = '\t' #tsv file format

# check if you can open mandatory input file
try:
    fhand1 = open( fname )
except:
    print('fileERR:', fileERR)
    raise SystemExit

###############################################################################
# Transpose input matrix counterclockwise. Return the results as a new matrix. 
###############################################################################

def transposeM(your_matrix):
    transposed_matrix = [ [your_matrix[j][i] for j in range(len(your_matrix))] for i in range(len(your_matrix[0])) ] 
    return(transposed_matrix)

##############################################################################


######################################
##### Read in process data ###########
######################################
# initialise matrix variable
#m = [ [] ]
m = [ ]

for line in fhand1:
    line = line.rstrip()
    m.append(line.split(delimiter))
#   # strip whitespace
#   refA = columns[0].strip() # reference allele sequence
#   altA = columns[1].strip() # variant allele sequence

#m = [['a',1,2],['b',3,4],['c',5,6]] 
for row in transposeM(m): 
#for row in m:
	print(row) 


# close file
fhand1.close()
