from tika import parser
import pandas as pd
import re

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
    ind_fin = string.find('2020')
    return string[ind_ini:ind_fin].split('\n')[-1]+'2020'

def parsing_table(string):
    first_number = re.search(r'\d+', string).group()
    new_lst = string.split(' ')
    ind = new_lst.index(first_number)
    final_list = [''.join(new_lst[:ind])]+new_lst[ind:]
    return [el for el in final_list if el != '']

def get_lst(string):
    ind_ini = string.lower().find('andalucía')
    ind_fin = string[ind_ini:].lower().find('total')
    list_tab = string[ind_ini:ind_ini+ind_fin].split('\n')
    list_tab = [el.replace(',','.') for el in [el.rstrip() for el in list_tab] if el != '']
    return [parsing_table(el) for el in list_tab]

def save_csv(lst, path):
    lst = get_lst(raw['content'])
    if len(lst[0])==5:
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
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"i:",["ifile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
    
    raw = parser.from_file(inputfile)
    fecha = get_fecha(raw['content'])
    lst = get_lst(raw['content'])
    save_csv(lst,'../data/csv_data/COVID_es_{}.csv'.format(fecha.replace('.','_')))

if __name__ == "__main__":
    main(sys.argv[1:])