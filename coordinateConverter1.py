#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Convert genomic coordinates between GRCh38 and GRCh37."""

__author__  = "Ray Stefancsik"
__version__ = "0.1"

######################################################################
# Import command-line parsing module from the Python standard library.
######################################################################
import argparse

#################################################################
# import modules recommended by
#### https://rest.ensembl.org/documentation/info/assembly_map
#################################################################
import requests
import sys
#################################################################

# input filename
fname = 'filename?'

parser = argparse.ArgumentParser( description='Convert genomic coordinates from GRCh38 to GRCh37 (default) or vice versa. All genomic coordinates are assumed to be on the positive strand. Input file is expected to be in a tabulated format (tsv/csv), e.g. :\n\t#chromosome   start   end\n\t17 36169091    36169091\n\tX 3084378 3084378', formatter_class=argparse.RawTextHelpFormatter )
parser.add_argument( 'input_file', help='Path to your input file.' )

# User options:
parser.add_argument('-v', '--verbose', help='Choose verbose output.', action='store_true')

# Optional, but mutually exclusive user options:
## genome build options
group1 = parser.add_mutually_exclusive_group()
group1.add_argument('-38', '--grch38', help='GRCh38 input assembly (default).', action='store_true')
group1.add_argument('-37', '--grch37', help='GRCh37 input assembly.', action='store_true')
## input file format options
group2 = parser.add_mutually_exclusive_group()
group2.add_argument('-t', '--tab', help='Use tab as column separator (default).', action='store_true')
group2.add_argument('-c', '--csv', help='Use comma as column separator.', action='store_true')

args = parser.parse_args()
# input filename
fname = args.input_file

##########################################################################
# define coordinate converter function
#################################################################
# https://rest.ensembl.org/documentation/info/assembly_map
# GET map/:species/:asm_one/:region/:asm_two
#################################################################
##########################################################################
def convertCoordinates( asmDirection, query_region ):
    """ Convert a set of genomic coordinates."""

    #################################################################
    #default values in case ENSEMBL api failed to map coordinates between genome assemblies:
    dfv = {
    'original': {
                    'seq_region_name': 'failed',
                    'start': 'failed',
                    'coord_system': 'chromosome',
                    'strand': 1,
                    'assembly': asm[0],
                    'end': 'failed'
                },
    'mapped': {
                    'seq_region_name': 'failed',
                    'start': 'failed',
                    'coord_system': 'chromosome',
                    'strand': 'failed',
                    'assembly': asm[1],
                    'end': 'failed'
              }
    }
    #default values in case ENSEMBL api finds multiple possible mapping coordinates between genome assemblies:
    dfv2 = {
    'original': {
                    'seq_region_name': 'multiple',
                    'start': 'multiple',
                    'coord_system': 'chromosome',
                    'strand': 1,
                    'assembly': asm[0],
                    'end': 'multiple'
                },
    'mapped': {
                    'seq_region_name': 'multiple',
                    'start': 'multiple',
                    'coord_system': 'chromosome',
                    'strand': 'multiple',
                    'assembly': asm[1],
                    'end': 'multiple'
              }
    }
    #################################################################

    server = 'https://rest.ensembl.org'
    ext1 = '/map/human/'
    asm_one = asmDirection[0]
    queryRegion = '/' + query_region[0] + ':' + query_region[1] + '..' + query_region[2] + ':1/'  # seq_region_name + start + stop
    asm_two = asmDirection[1] + '?'
     
    r = requests.get(server+ext1+asm_one+queryRegion+asm_two, headers={ "Content-Type" : "application/json"})
     
    if not r.ok:
      error1 = r.raise_for_status()
      decoded = error1
      
     
    decoded = r.json()


    if len( decoded['mappings']) == 1: # check if query region maps to a single locus
        mappings = ( decoded['mappings'][0] )
    elif len( decoded['mappings']) > 1: # check if query region maps to multiple sites
        mappings = dfv2
    else: # conversion has failed
        mappings = dfv

    return(mappings) # returns a dictionary like in the following example:
##########################################################################
#### {
#### 'original': {
####                 'seq_region_name': 'X',
####                 'start': 1000000,
####                 'coord_system': 'chromosome',
####                 'strand': 1,
####                 'assembly': 'GRCh38',
####                 'end': 1000100
####             },
#### 'mapped': {
####                 'seq_region_name': 'HG480_HG481_PATCH',
####                 'start': 960735,
####                 'coord_system': 'chromosome',
####                 'strand': '1',
####                 'assembly': 'GRCh37',
####                 'end': 960835
####           }
#### }
##########################################################################

#################################################################
# Parse user input,
# read in a data file and
# initialise global variables.
#################################################################
### Input file format:
if args.csv:
    delimiter = ',' #csv file format
else:
    delimiter = '\t' #tsv file format

### Direction of conversion
if args.csv:
    delimiter = ',' #csv file format
else:
    delimiter = '\t' #tsv file format

# genome assembly versions for the direction of conversion
asm_one = 'GRCh37'
asm_two = 'GRCh38'
if args.grch37:
    asm = tuple([asm_one, asm_two])
else:
    asm = tuple([asm_two, asm_one])

# open input file
try:
    fhand1 = open( fname )
except:
    print('File cannot be opened:', fname)
    exit()

# initialise variable to hold input
inputList = []
locus = tuple()
# Make an empty dictionary to hold unique query regions.
## This is to reduce the number of queries to the server in case of redundant query data.
loci = {}


# read in file line-by-line
for line in fhand1:
    if line.startswith('#'): # skip header line
        continue
    line = line.strip()
    columns = line.split(delimiter)
    if len(columns) > 1: # check if line is not empty
        locus = tuple(columns[:3])
        inputList.append(locus)
    else: # skip empty lines
        continue
    if locus in loci:
        continue
    else:
        loci[locus] = convertCoordinates( asm, locus )
# close file
fhand1.close()

#################################################################
# Format and print results
#################################################################
# verbose output?
if args.verbose:
    header = print( ' '.join(['#', asm[0], 'input coordinates']), 'Converted to assembly', 'seq_region_name', 'start', 'end', 'strand', sep='\t' )
    for i in inputList:
        results = [ loci[i]['mapped']['assembly'], loci[i]['mapped']['seq_region_name'], loci[i]['mapped']['start'], loci[i]['mapped']['end'], loci[i]['mapped']['strand'] ]
        inputCoordinates = list(i)
    #   print(i, loci[i] )
    #   print( i, '\t'.join( str(r) for r in results), sep='\t')
        print( ':'.join( str(c) for c in inputCoordinates), '\t'.join( str(r) for r in results), sep='\t')
    #   print( loci[i] )
else:
    header = print( ' '.join(['#', asm[1], 'seq_region_name']), 'start', 'end', sep='\t' )
    for i in inputList:
    #   results = [ loci[i]['mapped']['seq_region_name'], loci[i]['mapped']['start'], loci[i]['mapped']['end'], loci[i]['mapped']['assembly'], loci[i]['mapped']['strand'] ]
        results = [ loci[i]['mapped']['seq_region_name'], loci[i]['mapped']['start'], loci[i]['mapped']['end'] ]
        print( '\t'.join( str(r) for r in results), sep='\t')
