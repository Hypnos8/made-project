import os

from CrimeDataTransformation import CrimeDataCleaner
from DataFetcher import DataFetcher
from DataLoader import DataLoader
from La311DataTransformation import La311Cleaner
from project.PopulationDataTransformation import PopulationCleaner

# Between 0 and 1 - Defines relative amount of allowed invalid rows before raising a warning
total_invalid_threshold = 0.1
download_timeout_seconds = 500


class Pipeline:
    def __init__(self, total_invalid_threshold, download_timeout_seconds):
        # Set URLs fpr Download
        self.population_data_path = None
        self.url_la311 = "https://data.lacity.org/City-Infrastructure-Service-Requests/MyLA311-Service-Request-Data-2023/4a4x-mna2/about_data"
        self.url_crime_data = "https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8/about_data"
        self.url_zip_data = "https://www.kaggle.com/api/v1/datasets/download/cityofLA/los-angeles-county-shapefiles"
        self.url_street_data = "https://data.lacity.org/City-Infrastructure-Service-Requests/Street-Names/hntu-mwxc/about_data"
        self.url_population_data = "https://api.census.gov/data/2020/dec/dhc?get=group(P1)&ucgid=pseudo(0400000US06$8600000)"

        # Set timeouts
        self.total_invalid_threshold = total_invalid_threshold
        self.download_timeout_seconds = download_timeout_seconds
        # Set folders
        self.working_dir = os.getcwd()
        # Craft output_dir (data in parent directory)
        self.parent_dir = os.path.abspath(os.path.join(self.working_dir, os.pardir))

        # Paths of downloaded files
        self.la311_data_path = None
        self.crime_data_path = None
        self.street_data_path = None
        self.zip_data_path = None

        self.crime_data_transformation = CrimeDataCleaner(total_invalid_threshold)
        self.la311_data_transformation = La311Cleaner(total_invalid_threshold)
        self.population_data_transformation = PopulationCleaner(total_invalid_threshold)

        output_dir = os.path.join(self.parent_dir, "data")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        db_path = os.path.join(output_dir, "cleaned_db.sqlite")

        # Delete already existing db
        try:
            os.remove(db_path)
        except OSError:
            pass
        self.data_loader = DataLoader(db_path)



    def extract(self):
        data_fetcher = DataFetcher(self.working_dir)

        # Extract Data
        self.la311_data_path = data_fetcher.fetch_data_la_city(self.url_la311, "myla_data.csv",
                                                              self.download_timeout_seconds)
        self.crime_data_path = data_fetcher.fetch_data_la_city(self.url_crime_data, "crime_data.csv",
                                                              self.download_timeout_seconds)
        self.street_data_path = data_fetcher.fetch_data_la_city(self.url_street_data, "street_names.csv",
                                                               self.download_timeout_seconds)
        self.zip_data_path = data_fetcher.fetch_kaggle_geodata(self.url_zip_data, "CAMS_ZIPCODE_PARCEL_SPECIFIC.shp")
        self.population_data_path = data_fetcher.fetch_population_data(self.url_population_data, "population_data.csv",
                                                               self.download_timeout_seconds)



    def transform(self):
        # Transform Data
        self.crime_data_transformation.load_data(self.crime_data_path, self.zip_data_path, self.street_data_path)
        self.la311_data_transformation.load_data(self.la311_data_path)
        self.population_data_transformation.load_data(self.population_data_path)

        self.crime_data_transformation.transform_crimedata()
        self.la311_data_transformation.transform_data()
        self.population_data_transformation.transform_data()


    def load(self):

        self.data_loader.load_data(self.crime_data_transformation.data, "crime_data")
        self.data_loader.load_data(self.la311_data_transformation.data, "la311_data")
        self.data_loader.load_data(self.population_data_path.data, "population_data")

        return self.data_loader.path

    def set_default_file_path(self):
        self.la311_data_path = 'downloaded_data/myla_data.csv'
        self.crime_data_path = 'downloaded_data/crime_data.csv'
        self.street_data_path = 'downloaded_data/street_names.csv'
        self.zip_data_path = 'downloaded_data/CAMS_ZIPCODE_PARCEL_SPECIFIC.shp'
        self.population_data_path = 'downloaded_data/population_data.csv'



    def run_pipeline(self, do_extract=True):
        if do_extract:
            self.extract()
        else:
            self.set_default_file_path()
        self.transform()
        return self.load()


if __name__=="__main__":
    pipeline = Pipeline(total_invalid_threshold, download_timeout_seconds)
    pipeline.run_pipeline(do_extract=False)