#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Find publication title, DOI or PMID based on either the DOI or the PMID as the query term by using the Europe PMC API. """

__author__  = "Ray Stefancsik"
__version__ = "0.01"


######################################################################
# Import libraries to help work with JSON.
import jmespath
import json

######################################################################
# Import libraries to make API requests
import requests

######################################################################
# Import command-line parsing module from the Python standard library.
######################################################################
import argparse

parser = argparse.ArgumentParser( description='You must provide either a Digital Object Identifier or a PMID to query Europe PMC in a format starting with either "DOI:" or "EXT_ID", respectively. Keyword parameters are case insensitive. For example "doi:10.1016/j.stem.2019.12.005" or "ext_id:31928944".', formatter_class=argparse.RawTextHelpFormatter )
parser.add_argument( 'doi_OR_pmid', help='Use "doi:" for Digital Object Identifier queries. Use "ext_id:" for PMID queries.' )


args = parser.parse_args()


#################################################################
### Global variables to construct API endpoint strings
#################################################################
endpoint = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search'
# input argument
queryString = args.doi_OR_pmid


# endpoint example string: "https://api.ingest.archive.data.humancellatlas.org/submissionEnvelopes/5d1c67c688fa640008aff7cc/biomaterials"


def doi2pmid(query):
    """ Query Europe PMC API using a DOI. Return the associated PMID if it exists in the JSON returned by the API."""
    parameters = {
    'query' : query,
    'resultType' : 'lite', ## alternative: 'idlist',
    'cursorMark' : '*',
    'pageSize' : 25,
    'format' : 'json'
    }
    response = requests.get(endpoint, params = parameters)
#   print('endpoint:', response.url)
    data = response.json()
    foundTITLEs = jmespath.search('resultList.result[*].title', data)
    foundPMIDs = jmespath.search('resultList.result[*].pmid', data)
    foundDOIs = jmespath.search('resultList.result[*].doi', data)
    if len(foundTITLEs) == 1: # check if there is a single hit or not
        foundTitle = foundTITLEs[0]
    else:
        foundTitle = foundTITLEs
    if len(foundPMIDs) == 1: # check if there is a single hit or not
        foundPMID = foundPMIDs[0]
    else:
        foundPMID = foundPMIDs
    if len(foundDOIs) == 1: # check if there is a single hit or not
        foundDOI = foundDOIs[0]
    else:
        foundDOI = foundDOIs
    results = { 'TITLE' : foundTitle, 'PMID' : foundPMID, 'DOI' : foundDOI }
    return(results)

print ( 'Query:', queryString, 'Results:', doi2pmid(queryString))
