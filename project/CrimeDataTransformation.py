import geopandas

import pandas as pd
import numpy as np
import logging


class CrimeDataCleaner:
    def __init__(self, crime_data_path, geo_data_path, street_name_path, total_invalid_threshold):
        """

        :param crime_data_path: Path to file containing crime records
        :param geo_data_path: Path to file containing geographic information about ZIP code areas
        :param street_name_path: Path to List of Street names and suffixes
        :param total_invalid_threshold: Between 0 and 1 - Defines relative amount of allowed invalid rows (e.g with missing ZIP Code)
        """
        self.data = pd.read_csv(crime_data_path)
        self.zip_data = geopandas.read_file(geo_data_path)
        self.street_data = pd.read_csv(street_name_path, usecols=["Street Name", "Street Suffix"])

        self.rows_for_year = None
        self.total_invalid_threshold = total_invalid_threshold

    def __filter_by_year(self):
        time_pattern = r'\d{2}/\d{2}/2023'
        self.data = self.data[self.data["Date Occ"].str.contains(time_pattern)]

        self.rows_for_year = len(self.data)
        logging.info("After filtering by year there are ", self.rows_for_year, " rows")

        # Convert date of relevant rows from string to date
        self.data["Date Occ"] = pd.to_datetime(self.data["Date Occ"], format="%m/%d/%Y %I:%M:%S %p")

    def __adjust_column_names(self):
        self.data = self.data.rename(columns={"LOCATION": "Location",
                                              "DATE OCC": "Date Occ",
                                              "TIME OCC": "Time Occ",
                                              "AREA": "Area",
                                              "AREA NAME": "Area Name",
                                              "LAT": "Lat",
                                              "LON": "Lon",
                                              "DR_NO": "Dr No"
                                              })
        self.zip_data = self.zip_data.rename(columns={"ZIPCODE": "Zipcode"})
        self.street_data = self.street_data.rename(columns={"Street Name": "Street", "Street Suffix": "Suffix"})

    def __pre_drop_columns(self):
        self.data = self.data.drop(columns=['Part 1-2', 'Mocodes',
                                            'Status', 'Status Desc',
                                            'Date Rptd',
                                            'Crm Cd 1', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4'])

    def __transform_location(self):
        """
        Transform Location data by extracting.
        Tries to match missing street names in crime rcords using a list of available street names
        :return:
        """
        # remove trailing/leading whitespaces
        self.data["Location"] = self.data["Location"].str.strip()

        # remove multiple whitespaces
        self.data["Location"] = self.data["Location"].replace(r'\s+', ' ',regex=True)

        self.data[["Number", "Direction", "Street", "Suffix"]] = self.data["Location"].str.extract(
            r'^(?P<number>\d* )?(?P<direction>[NWSE] )?(?P<Street>\w+)(?P<Suffix> [A-Z]{2})?$')

        self.data = self.data.drop(columns=['Number', 'Direction'])  # We only take street and suffix into consideration

        # finding the corresponding suffix to a street name only works if it's unique
        # e.g we got "77th", but "77th ST" and "77th PL" exists, we can't restore it
        # --> we do not consider them for the lookup
        self.street_data = self.street_data.drop_duplicates(subset=['Street'], keep=False)

        # Rename "BLVD to BL" as used in the other dataset
        self.street_data[self.street_data["Suffix"] == "BLVD"] = "BL"
        self.data = self.data.merge(self.street_data, on="Street", how="left", suffixes=("_data", "_street"))
        self.data["Suffix"] = self.data["Suffix_data"].combine_first(self.data["Suffix_street"])

        empty_suffix = len(self.data[self.data["Suffix"].isna()])

    def __transform_crosstreet(self):
        self.data["Cross Street"] = self.data["Cross Street"].replace(r'\s+', ' ',regex=True)

    def __transform_gender(self):
        self.data["Vict Sex"] = self.data["Vict Sex"].str.strip()  # TODO Check why this causes a warning
        self.data.fillna({"Vict Sex": "X"}, inplace=True)
        self.data.loc[~self.data["Vict Sex"].isin(["F", "M", "X"]), "Vict Sex"] = "X"

    def __transform_vict_descent(self):
        self.data.fillna({"Vict Descent": "X"}, inplace=True)

    def __transform_vict_age(self):
        self.data.replace({"Vict Age": 0}, np.nan, inplace=True)

    def __get_zipcodes(self):

        # Load Data as geopandas frame with geometry data
        self.data = geopandas.GeoDataFrame(
            self.data,
            geometry=geopandas.points_from_xy(self.data.Lon, self.data.Lat),
            crs="EPSG:4326"
        )
        # Adjust type of coordinates if needed
        if self.zip_data.crs != self.data.crs:
            self.zip_data = self.zip_data.to_crs(self.data.crs)

        # Crime Incident is considered to be in ZIP Code Region if the corresponding geocordinates are within the area
        self.data = geopandas.sjoin(self.data, self.zip_data[['Zipcode', 'geometry']], how="left", predicate="within")

    def __show_statistics(self):
        """
        Calculate statistics and print them
        :return:
        """
        rows_without_zipcode = len(self.data[self.data["Zipcode"].isna()])
        rows_without_suffix = len(self.data[self.data["Suffix"].isna()])

        rows_after_processing = len(self.data)
        row_loss = self.rows_for_year - rows_after_processing
        total_invalid = rows_without_zipcode + row_loss + rows_without_suffix

        relative_row_loss = (row_loss / self.rows_for_year)
        relative_rows_missing_zipcode = rows_without_zipcode / self.rows_for_year
        relative_total_invalid = total_invalid / self.rows_for_year

        print("-- Crime Data --")
        msg_row_loss = "Loss of Rows during transformations: " + str(row_loss) + "(" + str(
            relative_row_loss * 100) + " %)"
        msg_missing_zipcode = ("Rows with missing Zip code:  " + str(rows_without_zipcode) +
                               "(" + str(relative_rows_missing_zipcode * 100) + " %)")
        msg_total_invalid = "Invalid rows: " + str(total_invalid) + "(" + str(relative_total_invalid * 100) + " %)"
        print(msg_row_loss)
        print(msg_missing_zipcode)
        print(msg_total_invalid)

        if relative_total_invalid > self.total_invalid_threshold:
            logging.warning("Exceeded Threshold for invalid rows!")

    def __post_drop_columns(self):
        self.data = self.data.drop(columns=['index_right', 'geometry', 'Suffix_street', 'Location', 'Suffix_data'])

    def __adjust_type_for_output(self):
        self.data = self.data.astype({'Premis Cd': 'Int64',
                                      'Weapon Used Cd': 'Int64',
                                      'Vict Age': 'Int64'
                                      })


    def transform_crimedata(self):
        # Only work with rows that are required for the project 
        # --> Crimes that occured in 2023
        self.__adjust_column_names()
        self.__filter_by_year()
        self.__pre_drop_columns()
        self.__transform_location()
        self.__transform_crosstreet()
        self.__transform_gender()
        self.__transform_vict_descent()
        self.__transform_vict_age()
        self.__get_zipcodes()
        self.__post_drop_columns()
        self.__adjust_type_for_output()
        self.__show_statistics()

    def save_dataset(self, output_path):

        self.data.to_csv(output_path, index=False)
