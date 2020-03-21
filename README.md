# COVID19 Spain cases

## Data
All raw data is directly downloaded from [Ministerio de Sanidad website](https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/situacionActual.htm), which daily updates the statistics from the COVID19 epidemy. The downloaded archives are PDF files that are transformed into csv files in order to better analyze them.

## Structure
```
.
├── data
│   ├── csv_data
│   ├── final_data
│   ├── info_data
│   └── pdf_data
├── imgs
├── notebooks
└── src
```

# Graphs
## Incidencia acumulada (casos/1000 hab)
![casos](https://github.com/victorvicpal/COVID19_es/blob/master/imgs/IA_200320.png)

## Models
### SIR model
![gif](https://github.com/victorvicpal/COVID19_es/blob/master/imgs/flatthecurve.gif)
