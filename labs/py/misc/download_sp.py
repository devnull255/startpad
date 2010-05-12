"""
Download all document links from a web page.
Used to extract all the docouments from a Sharepoint document library.

by Mike Koss, September, 2009

Notes:

9/14/09 mck:
Using Beautiful soup version 3.0.7a.  The current version (3.1.0.1) is NOT resilient
to the errors in my sharepoint document directory - since it uses the HTMLParser
module which itself raises an exception on reading a malformed tag.
"""

import os
import sys
import getopt
import re
import urllib
import urlparse

from BeautifulSoup import BeautifulStoneSoup

reExtensions = re.compile(r"^.*\.(docx?|xls|fla|swf|txt|jpg|jpeg|gif|png|pdf|zip|mdbx?|mht|xml)$", re.I)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:t:u:p:a:")
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    if len(opts) == 0:
        usage()
        sys.exit(2)

    targetDir = None

    for o, a in opts:
        if o == '-h':
            usage()
            sys.exit()
        if o == '-t':
            targetDir = a
        if o == '-d':
            url = a

    get_url_files(url, targetDir)
    
def usage():
    print "Usage: %s -d url [-h | -t target_dir]\n" % os.path.basename(sys.argv[0])
    print "Options\n"
    print "-h\t\t: help"
    print "-d\t\t: download the linked docments referenced on the web page"
    print "-t\t\t: target directory to place the files"

def get_url_files(url, targetDir=None):
    if targetDir is None:
        parts = urlparse.urlparse(url)
        targetDir = "%s_files" % parts[1]
    
    print "Scanning %s, copy files to -> %s" % (url, targetDir)

    (links, dirs) = extract_links(url)
    if len(links) == 0:
        print "No files to download."
    else:
        print "Found %d files to download." % len(links)
        download_files(links, targetDir)

    # Recursively download all the documents in sub-directories
    for (url, sDir) in dirs:
        get_url_files(url, "%s/%s" % (targetDir, sDir))

reSPDir = re.compile(r"^.*SubmitFormPost\(['\"](.+)&View=.*['\"]\).*$", re.I)
reSPPath = re.compile(r"^.*RootFolder=%2f(.*)$")

def extract_links(url):
    """
    Scan a web page for all the <a> tags referencing documents (must have one of the
    extensions in reExtensions).
    Returns an array of (fully qualified) urls to documents.
    """

    sock = urllib.urlopen(url)         
    htmlSource = sock.read()           
    sock.close()

    links = []
    dirs = []

    soup = BeautifulStoneSoup(htmlSource)

    for link in soup.findAll('a'):
        href = urlparse.urljoin(url, link['href'])
        if reExtensions.match(href) is None:
            continue
        links.append(href)

    links = list(set(links))

    mUrls = set()

    # SharePoint directories are not regular href's - pull path info from onclick javascript
    # Example onclick:
    #
    # javascript:ClearSearchTerm("{8EF6AB92-467B-410F-94E3-82048923368B}");
    #   javascript:SubmitFormPost("http://old.mit-club.org/WebContent/Forms/AllItems.aspx?
    #   RootFolder=%2fWebContent%2fDummy%20Folder&
    #   View=%7b8EF6AB92%2d467B%2d410F%2d94E3%2d82048923368B%7d");javascript:return false;
    for link in soup.findAll('a', href='javascript:SubmitFormPost()'):
        matchDir = reSPDir.match(link['onclick'])
        if matchDir is None:
            print "Error parsing onclick directory name: %r" % link['onclick']
            continue
        url = matchDir.group(1)
        if url in mUrls:
            continue
        mUrls.add(url)

        print "url: %s" % url
        matchPath = reSPPath.match(url)
        aPath = matchPath.group(1).split("%2f")
        dirs.append((url, aPath[-1]))

    return (links, dirs)

reFilename = re.compile("^.*\/([^\/]+)$")

def download_files(links, targetDir):
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)

    for link in links:
        parts = urlparse.urlparse(link)
        match = reFilename.match(parts[2])
        if match is None:
            raise Exception("Error processing file name: %s" % link)

        sFilename = "%s/%s" % (targetDir, match.group(1))
        if os.path.exists(sFilename):
            print "File exists (%s) - skipping" % sFilename
            continue
        else:
            print "Writing file: %s" % sFilename
        file = open(sFilename, 'wb')
        sock = urllib.urlopen(link)
        data = sock.read()  
        sock.close()
        file.write(data)
        file.close()

if __name__ == "__main__":
    main()
