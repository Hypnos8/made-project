# Project Plan

## Title
<!-- Give your project a short title. -->
Judging a book by its cover: Analyzing the relation between a disordered environment and crime in Los Angeles.

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
Do reported signs of disorder, such as graffiti or littering, correlate with crime in Los Angeles? 

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
When the Broken Window Theory was published in 1982, the relationship between a disordered environment and crime became subject to debate in the public sphere.
Since then, various case studies have been conducted that analyzed how restoring order in a certain area affects the number of crimes.
The goal of this project is to analyze whether more crimes are committed in disordered areas than in ordered ones.

To measure the degree of disorder, reports from MyLa311 from 2023 are used (DataSource1). 
MyLA311 is a platform provided by the City of Los Angeles that allows citizens to report issues like graffiti, illegal dumping, 
and homeless encampments. 
Information about reported incidents of crime in L.A. is provided by the Los Angeles Police Department (Datasource2) 
and includes location data. Only crimes that occurred in 2023 are considered.

The results of this analysis could provide insights into whether the common perception that more crimes occur in 'bad-looking' areas holds true.
This information could be valuable for both individuals and businesses, indicating whether avoiding disordered environments might mean avoiding crime hotspots.  


## Datasources

### Datasource1: Crime Data
* Metadata URL: https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8/about_data
* Data URL: https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8/data_preview
* Data Type: CSV

The data source is provided by the Los Angeles Police Department (LAPD). It reflects incidents of crime in Los Angeles since 2020. 

It was Last Updated on October 30, 2024.

Note: As the LAPD adapts to a new Record Management System, data  from  March 7th 2024 onward might not  include all incidents reported to the LAPD.

### Datasource2: MyLA311 Service Request Data
* Metadata URL: https://data.lacity.org/City-Infrastructure-Service-Requests/MyLA311-Service-Request-Data-2023/4a4x-mna2/about_data
* Data URL: https://data.lacity.org/City-Infrastructure-Service-Requests/MyLA311-Service-Request-Data-2023/4a4x-mna2/data_preview
* Data Type: CSV

The data source contains service request data from MyLA311 for requests that were submitted via phone, mobile apps, website, and other sources.

MyLA311 is a platform provided by the City of Los Angeles. It enables access to services of the city and the reporting of graffiti, street light problems and illegal dumping.

### Datasource3: Street Names

* Metadata URL: https://data.lacity.org/City-Infrastructure-Service-Requests/Street-Names/hntu-mwxc/about_data
* Data URL: https://data.lacity.org/City-Infrastructure-Service-Requests/Street-Names/hntu-mwxc/data_preview
* Data Type: CSV

Official Street Names in the City of Los Angeles. The dataset was  created and maintained by the Bureau of Engineering of L.A.

### Datasource4: ZIP Code Regions

* Metadata URL: https://www.kaggle.com/datasets/cityofLA/los-angeles-county-shapefiles/data
* Data URL: https://www.kaggle.com/api/v1/datasets/download/cityofLA/los-angeles-county-shapefiles
* Data Type: CSV

The data source contains ZIP Code boundary shapefiles for L.A.
They are provided by the City of Los Angeles at Kaggle.com and were uploaded in 2017.

The dataset was prefered over the actively maintained version version at  https://geohub.lacity.org/datasets/lacounty::la-county-zip-codes/about
as an automated downloading of the files from the portal does not work reliably.


## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Selection of data sources [#1][i1]
2. Exploration of data [#2][i2]
3. Dataset cleanup [#2][i2]
4. Data enrichment (location Information) [#3][i3]
5. Pattern analysis in data [#5][i5]
6. Reporting insights [#6][i6]


[i1]: https://github.com/Hypnos8/made-project/issues/1
[i2]: https://github.com/Hypnos8/made-project/issues/2
[i3]: https://github.com/Hypnos8/made-project/issues/3
[i4]:https://github.com/Hypnos8/made-project/issues/4
[i5]: https://github.com/Hypnos8/made-project/issues/5
[i6]: https://github.com/Hypnos8/made-project/issues/6
