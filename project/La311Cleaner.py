from collections import defaultdict

import numpy as np
import pandas as pd


class La311Cleaner:
    def __init__(self, crime_data_path):
        columns = ['SRNumber', 'CreatedDate',
                   'RequestType', 'Status', 'RequestSource', 'CreatedByUserOrganization',
                    'Anonymous',
                   'AddressVerified', 'ApproximateAddress', 'Address', 'Latitude', 'Longitude', 'APC', 'CD',
                   'NC', 'NCName', 'PolicePrecinct']

        types = {'SRNumber': 'object',
                 'CreatedDate': 'object',
                 'RequestType': 'object',
                 'Status': 'object',
                 'RequestSource': 'object',
                 'CreatedByUserOrganization': 'object',
                 'Anonymous': 'object',
                 'AddressVerified': 'object',
                 'ApproximateAddress': 'object',
                 'Address': 'object',
                 'Latitude': 'float64',
                 'Longitude': 'float64',
                 'APC': 'object',
                 'CD': 'Int64',
                 'NC': 'Int64',
                 'NCName': 'object',
                 'PolicePrecinct': 'object'}

        self.data = pd.read_csv(crime_data_path, usecols=columns, dtype=types)

    def filter_by_requestType(self):
        relevant_types = ['Single Streetlight Issue', 'Graffiti Removal', 'Illegal Dumping Pickup',
                          'Homeless Encampment']
        self.data = self.data.loc[self.data["RequestType"].isin(relevant_types)]

    def filter_by_year(self):
        time_pattern = r'\d{2}/\d{2}/2023'
        self.data = self.data[self.data["CreatedDate"].str.contains(time_pattern)]

        # debug!
    # self.data = self.data.iloc[:100]

    def transform_addressVerified(self):
        # According to documentation only Y/N allowed for this field.
        # Setting addresses to "not verified" unless it's cleary stated that they are
        self.data.loc[~self.data["AddressVerified"].isin(["Y", "N"]), "AddressVerified"] = "N"

    def save_dataset(self):
        self.data.to_csv("made_testeout_la.csv", index=False)

    def transform_data(self):
        self.filter_by_requestType()
        self.filter_by_year()
        self.transform_addressVerified()


cleaner = La311Cleaner("C:\\Users\\Eric\\Projects\\MADE\\made-project\\data\\myla_data.csv")
cleaner.transform_data()
cleaner.save_dataset()
