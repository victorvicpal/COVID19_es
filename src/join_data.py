#!/usr/bin/python

import pandas as pd
import os
import numpy as np
from scipy.integrate import odeint

##########################################
#                                        #
#    CSV > GLOBAL CSV --  Join csvs      #
#                                        #
##########################################


def date_lag(vect):
    days = np.array([el.day for el in vect])
    dif = days[1:] - days[:-1]
    return np.where(dif > 1)[0]


def get_splits(df, ind):
    return df.loc[:ind], df.loc[ind + 1:]


def get_new_lines(df, ind):
    lines = pd.DataFrame({
        'CCAA':
        df.loc[ind - 1:ind, 'CCAA'].values,
        'fecha': [
            df.loc[ind, 'fecha'] + pd.DateOffset(1),
            df.loc[ind, 'fecha'] + pd.DateOffset(2)
        ],
        'casos': [np.nan, np.nan],
        'IA': [np.nan, np.nan],
        'UCI': [np.nan, np.nan],
        'muertes': [np.nan, np.nan]
    })
    return lines


def get_line_eq(points):
    x_coords, y_coords = zip(*points)
    A = np.vstack([x_coords, np.ones(len(x_coords))]).T
    m, c = np.linalg.lstsq(A, y_coords, rcond=-1)[0]
    return m, c


def fill_gaps(df, var, ind, rnd):
    point0 = (df.loc[ind, 'fecha'].day, df.loc[ind, var])
    point1 = (df.loc[ind + 3, 'fecha'].day, df.loc[ind + 3, var])
    m, c = get_line_eq([point0, point1])
    val0 = np.round(m * df.loc[ind + 1, 'fecha'].day + c, rnd)
    val1 = np.round(m * df.loc[ind + 2, 'fecha'].day + c, rnd)
    return val0, val1


def CCAA_correction(df):
    df = df.reset_index(drop=True)
    ind = date_lag(df['fecha'])
    while len(ind) > 0:
        split1, split2 = get_splits(df, ind[0])
        lines = get_new_lines(df, ind[0])
        df = pd.concat([split1, lines, split2]).reset_index(drop=True)
        variables = list(df.columns)
        c = variables.index('fecha') + 1
        rounds = [0, 2, 0, 0]
        #for var, r in zip(variables[c:],rounds):
        #    df.loc[ind[0]+1, var], df.loc[ind[0]+2, var] = fill_gaps(df, var, ind[0], r)
        ind = date_lag(df['fecha'])
    return df

#def nuevos(line):
#    casos_hoy = line.values[1:]
#    casos_ayer = line.values[:-1]
#    return [np.nan]+list(casos_hoy-casos_ayer)


def main():
    csvs = [
        el for el in sorted(os.listdir('../data/csv_data/'), reverse=True)
        if 'csv' in el
    ]
    
    cols = ['CCAA','fecha','casos','nuevos','IA','Hospitalizados','HospitalizadosNuevos','UCI','UCINuevos',
            'muertes','muertesNuevos','curados','curadosNuevos','PCR','testrap']
    
    data = pd.DataFrame(columns=cols)
    
    for csv in csvs:
        data_int = pd.read_csv('../data/csv_data/{}'.format(csv),
                               engine='python')
        data = data.append(data_int, ignore_index=True).reset_index(drop=True)

    data.loc[data.loc[data.CCAA == '1'].index - 1, 'muertes'] = 1
    data = data.drop(data.loc[data.CCAA == '1'].index).reset_index(drop=True)
    data.loc[data.CCAA == 'Castilla-LaMancha', 'CCAA'] = 'CastillaLaMancha'

    data['fecha'] = pd.to_datetime(data['fecha'], format='%d.%m.%Y')
    data['casos'] = pd.to_numeric(data.casos)
    data['UCI'] = pd.to_numeric(data.UCI)

    data = data.sort_values(by=['CCAA', 'fecha']).reset_index(drop=True)

    #for CCAA in data.CCAA.unique():
    #    data.loc[data.CCAA == CCAA,'nuevos'] = nuevos(data.loc[data.CCAA == CCAA,'casos'])
    #    data.loc[data.CCAA == CCAA,'HospitalizadosNuevos'] = nuevos(data.loc[data.CCAA == CCAA,'Hospitalizados'])
    #    data.loc[data.CCAA == CCAA,'UCINuevos'] = nuevos(data.loc[data.CCAA == CCAA,'UCI'])
    #    data.loc[data.CCAA == CCAA,'muertesNuevos'] = nuevos(data.loc[data.CCAA == CCAA,'muertes'])
    #    data.loc[data.CCAA == CCAA,'curadosNuevos'] = nuevos(data.loc[data.CCAA == CCAA,'curados'])

    _data_ = pd.DataFrame(
        columns=['CCAA', 'fecha', 'casos', 'IA', 'UCI', 'muertes'])
    for CCAA in data.CCAA.unique():
        data_int = CCAA_correction(data[data.CCAA == CCAA])
        ind = data_int[data_int['fecha'] == '2020-03-13'].index[0]
        data_int.loc[ind + 1:ind + 2, 'IA'] = fill_gaps(data_int, 'IA', ind, 2)
        data_int.loc[ind + 1:ind + 2,
                     'UCI'] = fill_gaps(data_int, 'UCI', ind, 0)
        _data_ = _data_.append(data_int,
                               ignore_index=True).reset_index(drop=True)
        data['muertes'] = pd.to_numeric(data.muertes)

    del data
    data = _data_.copy()
    del _data_
    
    numcols = data.columns[2:]
    data[numcols] = data[numcols].apply(pd.to_numeric, errors='coerce')
    
    num = data._get_numeric_data()
    num[num < 0] = 0

    data.to_csv('../data/final_data/dataCOVID19_es.csv', index=False)
    print('dataCOVID19_es.csv updated')

if __name__ == "__main__":
    main()
