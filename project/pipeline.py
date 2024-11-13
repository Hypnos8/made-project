import os

from project.CrimeDataCleaner import CrimeDataCleaner
from project.DataFetcher import DataFetcher
from project.DataLoader import DataLoader
from project.La311Cleaner import La311Cleaner

# Between 0 and 1 - Defines relative amount of allowed invalid rows before raising a warning
total_invalid_threshold = 0.1
download_timeout_seconds = 500

# Used for temporary data
working_dir = os.getcwd()

# Craft output_dir (data in parent directory)
parent_dir = os.path.abspath(os.path.join(working_dir, os.pardir))
output_dir = os.path.join(parent_dir, "data")

## DEBUG
url_la311 = "https://data.lacity.org/City-Infrastructure-Service-Requests/MyLA311-Service-Request-Data-2023/4a4x-mna2/about_data"
url_crime_data = "https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8/about_data"
url_zip_data = "https://www.kaggle.com/api/v1/datasets/download/cityofLA/los-angeles-county-shapefiles"
url_street_data = "https://data.lacity.org/City-Infrastructure-Service-Requests/Street-Names/hntu-mwxc/about_data"

dataFetcher = DataFetcher(working_dir)

# Extract Data
la311_data_path = dataFetcher.fetch_data_la_city(url_la311, "myla_data.csv", download_timeout_seconds)
crime_data_path = dataFetcher.fetch_data_la_city(url_crime_data, "crime_data.csv", download_timeout_seconds)
street_data_path = dataFetcher.fetch_data_la_city(url_street_data, "street_names.csv", download_timeout_seconds)
zip_data_path = dataFetcher.fetch_kaggle_geodata(url_zip_data, "CAMS_ZIPCODE_PARCEL_SPECIFIC.shp")



# Transform Data
crime_data_cleaner = CrimeDataCleaner(crime_data_path, zip_data_path, street_data_path, total_invalid_threshold)
crime_data_cleaner.transform_crimedata()
la311_cleaner = La311Cleaner(la311_data_path, total_invalid_threshold)
la311_cleaner.transform_data()

# Load Data
db_path = os.path.join(output_dir, "cleaned_db.sqlite")
print("Saved results to " + db_path)
data_loader = DataLoader(db_path)
data_loader.load_data(crime_data_cleaner.data, "crime_data")
data_loader.load_data(la311_cleaner.data, "la311_data")
