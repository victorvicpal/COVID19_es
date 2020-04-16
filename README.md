# COVID19 Spain cases

## Data
All raw data is directly downloaded from [Ministerio de Sanidad website](https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/situacionActual.htm), which daily updates the statistics from the COVID19 epidemy. The downloaded archives are PDF files that are transformed into csv files in order to better analyze them.

## Repo Structure
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

## Data structure

```
data
├── csv_data
│   ├── COVID_es_[DATE].csv
├── final_data
│   └── dataCOVID19_es.csv
├── info_data
│   ├── PoblaciónCCAA.csv
│   ├── death_rate.csv
│   └── poblacio?\201n_edades.csv
└── pdf_data
    ├── Actualizacion_[XX]_COVID-19.pdf
```

* Original data are gathered in `data/pdf_data`
* csvs from original data by date are gathered in `data/csv_data`
* `info_data` contains extra data from sources such as [Instituto Nacional de Estadística](https://www.ine.es/)
* `final_data` contains the csv file `dataCOVID19_es.csv` which is daily updated.

### FINAL DATA (dictionary)

| Column        | Meaning       |
| ------------- |-------------:|
| CCAA          | Spanish Autonomous community |
| fecha         | Date          |
| casos         | Cases         |
| IA            | Cumulative incidence         |
| UCI           | Number of patients requiring Intensive care unit assistance        |
| muertes       | Number of deaths        |
| Hospitalizados      | Number of hospitalized patients      |
| curados      | Number of healed patients      |
| nuevos      | Number of new cases compared to the previous day       |

## Notebooks
The `notebooks` folder contains some examples of epidemologic models such as `SIRModel.ipynb`, `SEIRModel.ipynb` or `LogisticCurve.ipynb`.

## Contribute
Feel free to contact me or make a pull-request if you want to change/add anything.

**Special thanks to [Pedro Vélez](https://github.com/PedroVelez) and [covid-19-stats](https://github.com/covid-19-stats) for their contribution to this repo**
