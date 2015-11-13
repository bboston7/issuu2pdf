#!/usr/bin/env python3

import os
import sys

import urllib.error
import urllib.request

SWF_BASE = "http://page.issuu.com/{}/swf/page_{!s}.swf"

def get_swfs(doc_id):
    """ Given document id, download swfs and convert to pngs.
    Returns list of downloaded pngs"""

    page = 1
    downloaded = []
    try:
        while True:
            print("Attempting to download page " + str(page))
            print(SWF_BASE.format(doc_id,page))

            # Download page
            fname, _ = urllib.request.urlretrieve(SWF_BASE.format(doc_id, page))

            # Convert page to png
            print("Converting page " + str(page) + " to image")
            print()
            res = os.system("swfrender " + fname + " -o " + fname)
            assert res == 0

            # Record that we saved this file
            downloaded.append(fname)
            page += 1
    except urllib.error.HTTPError:
        print("Page " + str(page) + " does not exist.  Done downloading")

    return downloaded

def swf2pdf(files, outfile):
    print("Converting images to pdf " + outfile)
    inputs = " ".join(files)
    res = os.system("convert " + inputs + " " + outfile)
    assert res == 0

def get_doc_id(url):
    # Terrible way to parse HTML
    lines = urllib.request.urlopen(url).read().decode("utf8")
    for line in lines.split():
        if "page_1.jpg" in line:
            # Get doc_id
            tokens = line.split("/")
            doc_id = tokens[3]
            print("Found document id " + doc_id)
            return doc_id

def clean(files):
    for f in files:
        os.remove(f)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: " + sys.argv[0] + " url output-file")
        exit(1)

    url = sys.argv[1]
    outfile = sys.argv[2]

    doc_id = get_doc_id(url)
    files = get_swfs(doc_id)
    swf2pdf(files, outfile)
    clean(files)
