import logging
import pandas as pd


class La311Cleaner:
    def __init__(self, total_invalid_threshold):
        self.rows_for_year = None
        self.total_invalid_threshold = total_invalid_threshold
        self.data = None

    def load_data(self, crime_data_path):
        columns = ['SRNumber', 'CreatedDate',
                   'RequestType', 'Status', 'RequestSource', 'CreatedByUserOrganization', 'Anonymous',
                   'AddressVerified', 'ApproximateAddress', 'Latitude', 'Longitude', 'APC', 'CD',
                   'NC', 'NCName', 'PolicePrecinct', 'StreetName', 'Suffix', 'ZipCode']

        types = {'SRNumber': 'object',
                 'CreatedDate': 'object',
                 'RequestType': 'object',
                 'Status': 'object',
                 'RequestSource': 'object',
                 'CreatedByUserOrganization': 'object',
                 'Anonymous': 'object',
                 'AddressVerified': 'object',
                 'ApproximateAddress': 'object',
                 'StreetName': 'object',
                 'Suffix': 'object',
                 'Latitude': 'float64',
                 'Longitude': 'float64',
                 'APC': 'object',
                 'CD': 'Int64',
                 'NC': 'Int64',
                 'NCName': 'object',
                 'PolicePrecinct': 'object',
                 'ZipCode': 'object'}
        self.data = pd.read_csv(crime_data_path, usecols=columns, dtype=types)



    def __filter_by_request_type(self):
        # We're only interested in issues that affect the "visible disorder" of the enviornment
        relevant_types = ['Single Streetlight Issue', 'Graffiti Removal', 'Illegal Dumping Pickup',
                          'Homeless Encampment']
        self.data = self.data.loc[self.data["RequestType"].isin(relevant_types)]

    def __filter_by_year(self):
        time_pattern = r'\d{2}/\d{2}/2023'
        self.data = self.data[self.data["CreatedDate"].str.contains(time_pattern)]
        self.rows_for_year = len(self.data)

        # Convert date of relevant rows from string to date
        self.data["CreatedDate"] = pd.to_datetime(self.data["CreatedDate"], format="%m/%d/%Y %I:%M:%S %p")


        # debug!
    # self.data = self.data.iloc[:100]

    def __transform_address_verified(self):
        # According to documentation only Y/N allowed for this field.
        # Setting addresses to "not verified" unless it's cleary stated that they are
        self.data.loc[~self.data["AddressVerified"].isin(["Y", "N"]), "AddressVerified"] = "N"

    def save_dataset(self, output_file):
        self.data.to_csv(output_file, index=False)

    def __show_statistics(self):
        """
        Calculate statistics and print them
        :return:
        """
        rows_after_processing = len(self.data)

        rows_without_zipcode = len(self.data[self.data["Zipcode"].isna()])
        row_loss = self.rows_for_year - rows_after_processing
        total_invalid = rows_without_zipcode + row_loss

        relative_rows_missing_zipcode = rows_without_zipcode / self.rows_for_year
        relative_row_loss = (row_loss / self.rows_for_year)
        relative_total_invalid = total_invalid / self.rows_for_year

        print("-- La311 data -- ")
        msg_row_loss = "Loss of Rows during transformations: " + str(row_loss) + "(" + str(
            relative_row_loss * 100) + " %)"
        msg_missing_zipcode = ("Rows with missing Zip code:  " + str(rows_without_zipcode) +
                               "(" + str(relative_rows_missing_zipcode * 100) + " %)")
        print(msg_row_loss)
        print(msg_missing_zipcode)

        if relative_total_invalid > self.total_invalid_threshold:
            logging.warning("Exceeded Threshold for invalid rows!")

    def __adjust_column_names(self):
        self.data = self.data.rename(columns={"ZipCode": "Zipcode" })
    def transform_data(self):
        self.__filter_by_request_type()
        self.__filter_by_year()
        self.__adjust_column_names()
        self.__transform_address_verified()
        self.__show_statistics()
