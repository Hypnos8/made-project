# Analyzis of the relation between a disordered environment and crime in Los Angeles
This repository contains adata pipeline that retrieves data from Kaggle, the L.A. Data Catalog and the U.S. Portal to analyze the relationship between crime and a disordered enviroment in L.A. in 2023.
The results are presented in the analysis-report. All related files can be found in the folder `project`

In addition it contains all exercises for the Lecture Methods of Advanced Data Engineering offered at the FAU University Erlangen-Nürnberg in the folder `exercises`

## Project description
The goal of this project is to investigate whether more crimes are committed in disordered areas than in ordered ones. It therefore aims to answer the following question:

> **Do reported signs of disorder, such as graffiti, correlate with crime in Los Angeles in 2023?**

The results of this analysis could provide insights into whether the common perception that more crimes occur in bad-looking areas holds true. This information could be valuable for both individuals and businesses, indicating whether avoiding disordered environments might mean avoiding crime hotspots.

### Pipeline Architecture
the data is firstly fatched by the data_fetcher. Afterwards the crime and MyLa311 data are transformed by their respective transformer object. 
Transformations include removing invalid values, adding missing values such as missing street name suffixes and preparing the data by mapping GPS coordinates to a ZIP code region for further analyzsis.

The transformed data is loaded into a SQLite file.
![Pipeline architecture](data-pipeline.jpg)

# Licencse
This project uses different licenses for code (i.e. python code and notebooks) and data.

## Source Code 
The source code is licensed under the MIT License (see `README-MIT`).

## Data 

Data is licensed  under a 
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-shield]][cc-by]
[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
