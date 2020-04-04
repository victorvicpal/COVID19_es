#!/usr/bin/python

from tika import parser
import pandas as pd
import re
import sys, getopt
import numpy as np

###############################################
#                                             #
#    From PDF to CSV -- Based on structured   #
#    reports from Actualizacion_37 and only   #
#    for weekly updates. Weekend documents    #
#    do not have a specific format.           #
#                                             #
###############################################

def get_fecha(string):
    ind_ini = string.find('(COVID-19)')
    ind_fin = string.find('.20')
    return string[ind_ini:ind_fin].split('\n')[-1]+'.2020'

def parsing_table(string):
    first_number = re.search(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', string).group()
    new_lst = string.split(' ')
    ind = new_lst.index(first_number)
    final_list = [''.join(new_lst[:ind])]+new_lst[ind:]
    return [el for el in final_list if el != '']

def get_lst(string):
    ind_ini = string.lower().find('andalucía')
    ind_fin = min(string[ind_ini:].lower().find('total'),string[ind_ini:].lower().find('españa'))
    list_tab = string[ind_ini:ind_ini+ind_fin].split('\n')
    list_tab = [el.replace('.','') for el in [el.rstrip() for el in list_tab] if el != '']
    list_tab = [el.replace(',','.') for el in [el.rstrip() for el in list_tab] if el != '']
    return [parsing_table(el) for el in list_tab]

def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))

def justNumbers(inputString):
    return re.search(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', inputString).group()

def save_csv(lst, fecha, path):
    if len(lst[0])==8:
        cols = ['CCAA', 'casos', 'IA','Hospitalizados', 'UCI', 'muertes', 'curados','nuevos']
    elif len(lst[0])==7:
        cols = ['CCAA', 'casos', 'IA','Hospitalizados', 'UCI', 'muertes', 'nuevos']
    elif len(lst[0])==5:
        cols = ['CCAA', 'casos', 'IA', 'UCI', 'muertes']
    elif len(lst[0])==4:
        cols = ['CCAA', 'casos', 'IA', 'UCI']
    elif len(lst[0])==3:
        cols = ['CCAA', 'casos', 'IA']
    data = pd.DataFrame(lst, columns = cols)
    data['fecha'] = [fecha]*data.shape[0]
    cols.insert(1, 'fecha')
    data[cols].to_csv(path, index=False)
    
def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"i:",["ifile="])
    except getopt.GetoptError:
        print('pdf_to_csv.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg

    rawdata = parser.from_file(inputfile)
    fecha = get_fecha(rawdata['content'])
    lst = get_lst(rawdata['content'])
    
    for i, l in enumerate(lst):
        for j, el in enumerate(l):
            if hasNumbers(el):
                lst[i][j] = justNumbers(el)
            else:
                lst[i][j] = el
    
    save_csv(lst, fecha,'../data/csv_data/COVID_es_{}.csv'.format(fecha.replace('.','_')))
    print('COVID_es_{}.csv created'.format(fecha.replace('.','_')))

if __name__ == "__main__":
    main(sys.argv[1:])