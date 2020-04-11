#!/usr/bin/python

import sys, getopt
import os
import requests
from bs4 import BeautifulSoup
import re

###############################################
#                                             #
#    Download PDF from Ministerio de Sanidad  #
#                                             #
###############################################


def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True, verify=False) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    print(local_filename)
    return local_filename


def main(argv):
    url = ''
    try:
        opts, args = getopt.getopt(argv, "u:", ["url="])
    except getopt.GetoptError:
        print('download_pdf.py -u <url>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-u", "--url"):
            url = arg

    download_file(url)
    print('file downloaded')

    lst_files = [file for file in os.listdir() if 'Act' in file]
    if os.path.isdir("../data/pdf_data/"):
        for f in lst_files:
            os.rename("./{}".format(f), "../data/pdf_data/{}".format(f))
    else:
        os.mkdir("../data/pdf_data/")
        for f in lst_files:
            os.rename("./{}".format(f), "../data/pdf_data/{}".format(f))


if __name__ == "__main__":
    main(sys.argv[1:])
