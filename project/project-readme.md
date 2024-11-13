# Technical Specs of this project
## Outline
This ETL-Pipeline performs the following steps
1. Download Data from LA31, Crime Data, Street Name Data and ZIP area date --> `DataFetcher.py`
2. Enrich crime data 
   3. Enrich with ZIP Codes
   4. extract Street Names from Locations 
   5. Fix street names missing Suffix (if possible)
   5. general data cleanup 
   6. --> `CrimeDataCleaner.py`
3. La311 Data
   4. Clean UP
   5. --> `La311Cleaner.py`
4. Load Data in SQL Database

## Good to know
* Downloading La311 takes a few minutes -> If you have a very slow connection consider adjusting the timeout in `pipeline.py`
* Not all Street Suffix can be reconsturced (see comment in COde)