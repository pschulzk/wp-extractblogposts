import sys
import os
import os.path
import re
import unicodedata
import time
import datetime
import urllib2
import json
import sched
import uuid
from enum import Enum

# WP Get Blog ################################################

############ CONSTANTS

BLOG_URL = ''

# Shell parameter: run mode -> dev mode (reset all database!)
if len(sys.argv) > 1:
    BLOG_URL = sys.argv[1]
else:
    raise ValueError( 'Missing parameter: WorPress blog domain. E. g. "https://myblog.com"' )


############ METHODS

def httpGet(url):
    response_body = urllib2.urlopen( url ).read()
    response_dictionary = json.loads( response_body )
    return response_dictionary

def getPosts():
    return httpGet(BLOG_URL + '/wp-json/wp/v2/posts?per_page=100&author=1')

def getFeaturedImagesLinks(response):
    featuredImagesLinks = []
    for val in response:
        try:
            featuredImagesLinks.append(val['_links']['wp:featuredmedia'][0]['href'])
        except:
            pass

    featuredImagesLinksResolved = []
    for val in featuredImagesLinks:
            try:
                featuredImagesLinksResolved.append(getFeaturedImagesLinkResolved(val))
            except:
                pass
    print featuredImagesLinksResolved

def getFeaturedImagesLinkResolved(url):
    mediaData = httpGet(url)
    print mediaData['source_url']
    return mediaData['source_url']

############ EXECUTE

getFeaturedImagesLinks( getPosts() )