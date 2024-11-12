import DataFetcher
import pandas as pd
from geopy.geocoders import Nominatim
import numpy as np

def download_data():
    dataFetcher = DataFetcher.DataFetcher()
    test_data_path = dataFetcher.fetch_data( 
                "https://data.lacity.org/Community-Economic-Development/Department-of-Recreation-and-Parks-Facility-and-Pa/ax8j-dhzm/about_data",
                "mytest.csv"
                )
    myla_data_path = dataFetcher.fetch_data( 
                "https://data.lacity.org/City-Infrastructure-Service-Requests/MyLA311-Service-Request-Data-2023/4a4x-mna2/about_data",
                "myla_data.csv"
                )
    crime_data_path = dataFetcher.fetch_data( 
                "https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8/about_data",
                "crime_data.csv"
                )
  
    dataFetcher.cleanup()

class CrimeDataCleaner():
    def __init__(self, crime_data_path) :
        self.data = pd.read_csv(crime_data_path)

    def filter_by_year(self):
        time_pattern = r'\d{2}/\d{2}/2023'
        self.data = self.data[self.data["Date Occ"].str.contains(time_pattern)]

        # debug!
        self.data = self.data.iloc[:100]

    def adjust_column_names(self):
        self.data = self.data.rename(columns={"LOCATION": "Location",
                                              "DATE OCC": "Date Occ",
                                              "Time OCC": "Time Occ",
                                              "AREA": "Area",
                                              "AREA NAME": "Area Name",
                                              "LAT": "Lat",
                                              "LON": "Lon",
                                              "Time OCC": "Time Occ",

        })

    def drop_columns(self):
        self.data = self.data.drop(columns=['Part 1-2', 'Mocodes',
                                            'Status', 'Status Desc',
                                            'Date Rptd',
                                            'Crm Cd 1', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4'])
    

    def transform_location(self):
        # remove trailing/leading whitespaces
        self.data["Location"] = self.data["Location"].str.strip() # TODO Check why this causes a warning

        # remove multiple whitespaces
        self.data["Location"] = self.data["Location"].replace(r'\s+', ' ', regex=True) # TODO Check why this causes a warning

    def transform_geocoordinates(self):
        # Query GPS data from Nominatim (for missing GPS values)

        geolocator = Nominatim(user_agent="MADE-project")
        for i in self.data[(self.data["Lat"] == 0) | (self.data["Lon"] == 0)].index:
            location = geolocator.geocode(self.data["LOCATION"][i] + ", Los Angeles")
            if location:
                self.data["Lat"][i] = location.latitude
                self.data["Lon"][i] = location.longitude
            else:
                print("Failed to enrich case " + self.data["DR_NO"][i])
                # Todo Think of strategy  what to do with bad ones

    def transform_crosstreet(self):
        self.data["Cross Street"] = self.data["Cross Street"].replace(r'\s+', ' ', regex=True) # TODO Check why this causes a warning
    
    def transform_gender(self):
        self.data["Vict Sex"] = self.data["Vict Sex"].str.strip() # TODO Check why this causes a warning
        self.data.fillna({"Vict Sex": "X"},inplace=True)
        self.data.loc[~self.data["Vict Sex"].isin(["F", "M", "X"]), "Vict Sex"] = "X"

    def transform_vict_descent(self):
        self.data.fillna({"Vict Descent":"X"},inplace=True)

    def transform_vict_age(self):
        self.data.replace({"Vict Age": 0}, np.nan, inplace=True)


    def transform_crimedata(self):
        # Only work with rows that are required for the project 
        # --> Crimes that occured in 2023
        self.adjust_column_names()
        self.filter_by_year()
        self.drop_columns()
        self.transform_location()
        self.transform_crosstreet()
        self.transform_gender()
        self.transform_vict_descent()
        self.transform_vict_age()
        self.transform_geocoordinates()

    def save_dataset(self):
        self.data = self.data.astype({'Premis Cd': 'Int64',
                                      'Weapon Used Cd': 'Int64',

                                      'Vict Age': 'Int64'
                                      })
        self.data.to_csv("made_testeout.csv", index=False)

crime = CrimeDataCleaner("C:\\Users\\Eric\\Projects\\MADE\\made-project\\data\\crime_data.csv")
crime.transform_crimedata()
crime.save_dataset()

