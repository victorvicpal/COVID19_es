#!/usr/bin/python

import os
import requests
from bs4 import BeautifulSoup
import re

###############################################
#                                             #
#    PDF updates from Ministerio de Sanidad   #
#                                             #
###############################################


def get_file_names(url):
    try:
        req_page = requests.get(url, stream=True, verify=True)
    except Exception as e:
        raise Exception(f"Could not get web page content: {e}")

    re_pdf = re.compile(r"(documentos/.+?\.pdf)")

    pdf_paths = list(set(re_pdf.findall(req_page.text)))
    return pdf_paths


def main():
    DAILY_FOLDER = "../data/pdf_data/"
    ES_REPORT_URL = "https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/situacionActual.htm"
    PDF_BASE_URL = "https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/"

    pdf_paths = [
        PDF_BASE_URL + i for i in get_file_names(ES_REPORT_URL)
        if "Informacion_inicial_alerta" not in i
    ]

    for pdf_path in pdf_paths:
        pdf_name = pdf_path.split("/")[-1]
        pdf_path_get = requests.get(pdf_path, stream=True, verify=False)
        with open(os.path.join(DAILY_FOLDER, pdf_name), 'wb') as f:
            f.write(pdf_path_get.content)

    lst_files = [file for file in os.listdir() if 'Act' in file]
    if os.path.isdir("../data/pdf_data/"):
        for f in lst_files:
            os.rename("./{}".format(f), "../data/pdf_data/{}".format(f))
    else:
        os.mkdir("../data/pdf_data/")
        for f in lst_files:
            os.rename("./{}".format(f), "../data/pdf_data/{}".format(f))


if __name__ == "__main__":
    main()
