# Project Plan

## Title
<!-- Give your project a short title. -->
Judging a book by its cover: Analyzing the relation between a disordered environment and crime in Los Angeles.

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
1. Do reported signs of disorder,like graffiti or littering, correlate with crime in Los Angeles? 

## Description
## Title
<!-- Give your project a short title. -->
Judging a book by its cover: Analyzing the relation between a disordered environment and crime in Los Angeles.

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
Do reported signs of disorder,like graffiti or littering, correlate with crime in Los Angeles? 

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
When the broken window theory was published in 1982 the relation between a disordered environment and crime became subject to debate in the public sphere.
Since then various case studies have been conducted that analyzed how restoring order in a certain area affects the number of crimes.
However, The goal of the following project is to analyze whether more crimes are committed in disordered areas than in ordered ones.

To measure the degree of disorder reports from MyLa311 from 2023 are used (DataSource1). 
MyLA311 is a platform provided by the City of Los Angeles that allows citizens to report issues like graffiti, waste dumps, 
and homeless encampments. 
The information about reported incidents of crime in L.A. is provided by the Los Angeles Police Department (Datasource2) 
and also contains location data. 

The results can give insights whether the widespread idea that more crimes happen in "bad looking areas" holds true.
This insight can be useful for individuals as well as businesses as it indicates whether avoiding disordered environments means avoiding crime hotspots.  


## Datasources

### Datasource1: Crime Data
* Metadata URL: https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8/about_data
* Data URL: https://github.com/Hypnos8/made-project/blob/main/project/Crime_Data_from_2020_to_Present_20241105.zip
* Data Type: Zip -> CSV

The data Source is provided by the Los Angeles Police Department (LAPD). It reflects incidents of crime in Los Angeles since 2020. 

It was Last Updated on October 30, 2024. 
Note: As the LAPD adapts to a new Record Management Systems the data starting from  March 7th 2024 might not  contain all all incidents reported to the LAPD.

### Datasource2: MyLA311 Service Request Data
* Metadata URL: https://data.lacity.org/City-Infrastructure-Service-Requests/MyLA311-Service-Request-Data-2023/4a4x-mna2/about_data
* Data URL: https://github.com/Hypnos8/made-project/blob/main/project/MyLA311_Service_Request_Data_2023_20241106.zip
* Data Type: Zip -> CSV

The data Source contains service request data from MyLA311 for requests that were submitted via phone, mobile apps, website and other sources.

MyLA311 is a platform provided by the City of Los Angeles. It enables access to services of the city and the reporting of graffiti, street light problems and illegal waste dumps.

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Selection of Data sources [#1][i1]
2. Exploration of data[#2][i2]
3. Clean-Up of the Dataset[#2][i2]
4. Enrichment of data (location Information)[#3][i3]
5. Analyzing patterns in Data[#5][i5]
6. Reporting of insights[#6][i6]


[i1]: https://github.com/Hypnos8/made-project/issues/1
[i2]: https://github.com/Hypnos8/made-project/issues/2
[i3]: https://github.com/Hypnos8/made-project/issues/3
[i4]:https://github.com/Hypnos8/made-project/issues/4
[i5]: https://github.com/Hypnos8/made-project/issues/5
[i6]: https://github.com/Hypnos8/made-project/issues/6
