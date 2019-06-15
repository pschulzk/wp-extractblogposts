################################################ WP Extract Blog Posts

############ IMPORTS
import sys
import os
import os.path
import urllib
import urllib2
import json

############ VARIABLES

BLOG_URL = ''
OUTPUT_DIR = os.getcwd() + '/output'
PYTHON_ENCODING = 'utf-8'
COUNTER = 0

# Shell parameter: run mode -> dev mode (reset all database!)
if len(sys.argv) > 1:
    BLOG_URL = sys.argv[1]
else:
    raise ValueError( 'Missing parameter: WorPress blog domain. E. g. "https://myblog.com"' )


############ METHODS

def httpGetJson(url):
    response_body = urllib2.urlopen( url ).read()
    response_dictionary = json.loads( response_body )
    return response_dictionary

def getPosts():
    return httpGetJson(BLOG_URL + '/wp-json/wp/v2/posts?per_page=100')

def getFeaturedImagesLinkResolved(url):
    mediaData = httpGetJson(url)
    return mediaData['source_url']

def getPostContents(response):
    # get featured images links and blog contents
    for val in response:
        global COUNTER

        try:
            blogTitle = val['title']['rendered'].encode( PYTHON_ENCODING )
            featuredImageUrl = getFeaturedImagesLinkResolved(val['_links']['wp:featuredmedia'][0]['href'])
            print featuredImageUrl
            blogContent = val['content']['rendered'].encode( PYTHON_ENCODING )

            currentDir = OUTPUT_DIR + '/' + blogTitle
            os.mkdir( currentDir )

            # download and save blogpost's featured image
            urllib.urlretrieve( featuredImageUrl, currentDir + '/' + blogTitle + '.jpg' )

            with open( currentDir + '/' + blogTitle + '.html', 'w+' ) as f:
                f.write( '<h1>' + blogTitle + '</h1>' + blogContent )
                f.close()

            COUNTER += 1

        except IOError:
            raise IOError

def run():
    print '### WP EXTRACT BLOG POSTS: running...'
    getPostContents( getPosts() )
    print '### WP EXTRACT BLOG POSTS: Successfully extracted ' + str(COUNTER) + ' blogposts from ' + BLOG_URL

############ EXECUTE

run()