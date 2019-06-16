################################################ WP Extract Blog Posts

############ IMPORTS
import json
import os
import sys
import urllib
import urllib2

############ VARIABLES

BLOG_URL = ''
OUTPUT_DIR = os.getcwd() + '/output'
PYTHON_ENCODING = 'utf-8'
COUNTER = 0

############ SHELL PARAMETER

if len( sys.argv ) > 1:
    BLOG_URL = sys.argv[ 1 ]
else:
    raise ValueError( 'Missing parameter: WordPress blog domain. E. g. "https://myblog.com"' )


############ METHODS

def httpGetJson( url ):
    response_body = urllib2.urlopen( url ).read()
    response_dictionary = json.loads( response_body )
    return response_dictionary

def getPosts():
    return httpGetJson( BLOG_URL + '/wp-json/wp/v2/posts?per_page=100' )

def getFeaturedImagesLinkResolved( url ):
    mediaData = httpGetJson(url)
    return mediaData['source_url']

def getPostContents( response ):
    # get featured images links and blog contents
    for val in response:
        global COUNTER

        try:
            blogTitle = val[ 'title' ][ 'rendered' ].encode( PYTHON_ENCODING )
            blogContent = val[ 'content' ][ 'rendered' ].encode( PYTHON_ENCODING )

            currentDir = OUTPUT_DIR + '/' + blogTitle
            os.mkdir( currentDir )

            with open( currentDir + '/' + blogTitle + '.html', 'w+' ) as f:
                f.write( '<h1>' + blogTitle + '</h1>' + blogContent )
                f.close()

            # download and save blogpost's featured image if exist
            try:
                featuredImageUrl = val[ '_links' ][ 'wp: featuredmedia'][ 0 ][ 'href' ]
                featuredImagesLinkResolved = getFeaturedImagesLinkResolved( featuredImageUrl )
                urllib.urlretrieve( featuredImagesLinkResolved, currentDir + '/' + blogTitle + '.jpg' )
            except:
                pass

            print '### WP EXTRACT BLOG POSTS: downloaded "' + blogTitle + '"'
            COUNTER += 1

        except IOError:
            pass

def run():
    print '### WP EXTRACT BLOG POSTS: running...'
    getPostContents( getPosts() )
    print '### WP EXTRACT BLOG POSTS: Successfully extracted ' + str( COUNTER ) + ' blogposts from ' + BLOG_URL

############ EXECUTE

run()