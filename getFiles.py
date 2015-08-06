'''
Author: Kevin Heath

Description:
    Short script to download all files of a specified type
    from a website (that requires no user identification).

    Run: python getFiles.py website filetype
'''

import urllib2
from bs4 import BeautifulSoup
import urlparse
import os.path
import sys, io


def main(argv):
    url = argv[0]
    fType = argv[1]
    print 'url is: '+url
    urlParts = urlparse.urlsplit(url)
    urlOb = urllib2.urlopen(url) 
    print 'Found url'
    html = urlOb.read()
    parsed_html = BeautifulSoup(html, 'html.parser')
    
    numFiles = 0
    for link in parsed_html.find_all('a', href=True):
        fLink = link.get('href')
        if fLink.endswith(fType):
            fLink = url+fLink
            fileName = fLink.split('/')[-1].split('#')[0].split('?')[0]
            if downloadFile(fLink, fileName, numFiles):
                numFiles+=1

    print 'Downloaded '+str(numFiles)+' files.'


def downloadFile(fileLoc, fileName, number):
    urlOb = urllib2.urlopen(fileLoc)
    
    file_size = int(urlOb.info()['content-length'])             #getting size in bytes of file(pdf,mp3...)
    print "Downloading: %s Bytes: %s" % (fileName, file_size)
 
    downloaded = 0
    block_size = int(file_size/10)       #bytes to be downloaded in each loop till file pointer does not return eof
    try:
        if os.path.isfile(fileName):
            fileName  = str(number)+fileName
        with open(fileName, 'wb') as handle:
            while True:
                buff = urlOb.read(block_size)
                if not buff:                                             #file pointer reached the eof
                   break
                downloaded = downloaded + len(buff)
                handle.write(buff)
                download_status = int(downloaded * 100.00 / file_size)
                print str(download_status)+"% done"
        return True
    except:
        return False

if __name__ == "__main__":
   main(sys.argv[1:])