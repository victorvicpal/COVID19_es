#!/usr/bin/python

from tika import parser
import pandas as pd
import re
import sys, getopt
import numpy as np

######################################
#                                    #
#    From PDF to CSV -- Age TABLE    #
#                                    #
######################################

def get_age_tables(string, keywords):
    tabs = []
    for kw in keywords:
        i1 = string.find(kw)
        i1 = i1 + string[i1:].find('0-9')
        i2 = i1 + string[i1:].find('Total')
        tabs.append(string[i1:i2])
    return tabs

def str_cln(string):
    string = string.replace('90 y +', '90+').replace('.', '').replace(',', '.').replace('\n', '')
    return string

def get_lines(string):
    age_lst = ['0-9','10-19','20-29','30-39','40-49','50-59','60-69',
                '70-79','80-89','90+']
    
    lst = [string[string.find(age):string.find(age_lst[i+1])] for i, age in enumerate(age_lst[:-1])]
    fin = [string[string.find('90+'):]]
    return lst + fin

def get_fecha(string):
    ind_ini = string.find('(COVID-19)')
    ind_fin = string.find('.20')
    return string[ind_ini+12:ind_fin].split('\n')[-1]+'.2020'

def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))

def hasCharacters(inputString):
    return bool(re.search(r'[a-zA-Zñáéíóú]+', inputString))

def justNumbers(inputString):
    return re.search(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', inputString).group()

def justCharacter(inputString):
    return re.search("[a-zA-Zñáéíóú]+", inputString).group()

def cleanlst(lista):
    for i, l in enumerate(lista):
        inddel = ind_empty_spc(l)
        if inddel:
            [l.pop(i) for i in inddel]
        for j, el in enumerate(l):
            if j != 0:
                if hasNumbers(el):
                    lista[i][j] = justNumbers(el)
                elif hasCharacters(el):
                    lista[i][j] = justCharacter(el)
                else:
                    lista[i][j] = el
    return lista

def parse_lst(lst):
    lst = [l.split(' ') for l in lst]
    return lst

def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "i:", ["ifile="])
    except getopt.GetoptError:
        print('pdf_to_csv.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg

    raw = parser.from_file(inputfile)
    
    tot, muj, hom = get_age_tables(raw['content'], ['Grupo de', 'Grupo de', 'Grupo de'])
    
    listt = cleanlst(parse_lst(get_lines(str_cln(tot))))
    listm = cleanlst(parse_lst(get_lines(str_cln(muj))))
    listh = cleanlst(parse_lst(get_lines(str_cln(hom))))
    
    colst = ['age', 'ConfT', 'HospT','HospT%', 'UCIT', 'UCIT%', 'FallT', 'FallT%', 'LetT','drop']
    colsm = ['age', 'ConfM', 'HospM','HospM%', 'UCIM', 'UCIM%', 'FallM', 'FallM%', 'LetM','drop']
    colsh = ['age', 'ConfH', 'HospH','HospH%', 'UCIH', 'UCIH%', 'FallH', 'FallH%', 'LetH','drop']
    
    datat = pd.DataFrame(listt, columns = colst).drop('drop', axis=1)
    datam = pd.DataFrame(listm, columns = colsm).drop('drop', axis=1)
    datah = pd.DataFrame(listh, columns = colsh).drop('drop', axis=1)
    
    data = pd.merge(datat,datam, on='age')
    data = pd.merge(data,datah, on='age')
    
    fecha = get_fecha(raw['content'])
    data['fecha'] = fecha
    
    cols = ['age', 'fecha', 'ConfT', 'HospT', 'HospT%', 'UCIT', 'UCIT%', 'FallT', 'FallT%',
       'LetT', 'ConfM', 'HospM', 'HospM%', 'UCIM', 'UCIM%', 'FallM', 'FallM%',
       'LetM', 'ConfH', 'HospH', 'HospH%', 'UCIH', 'UCIH%', 'FallH', 'FallH%',
       'LetH']
    
    data[cols].to_csv('../../data/csv_agedata/COVID_AGE_es_{}.csv'.format(fecha.replace('.', '_')), index=False)
    print('COVID_AGE_es_{}.csv created'.format(fecha.replace('.', '_')))

if __name__ == "__main__":
    main(sys.argv[1:])
