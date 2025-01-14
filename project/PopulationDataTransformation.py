import logging
import pandas as pd


class PopulationCleaner:
    def __init__(self, total_invalid_threshold):
        self.rows_for_year = None
        self.total_invalid_threshold = total_invalid_threshold
        self.data = None
        self.columns =  ['SRNumber', 'CreatedDate',
                   'RequestType', 'Status', 'RequestSource', 'CreatedByUserOrganization', 'Anonymous',
                   'AddressVerified', 'ApproximateAddress', 'Latitude', 'Longitude', 'APC', 'CD',
                   'NC', 'NCName', 'PolicePrecinct', 'StreetName', 'Suffix', 'ZipCode']

    def load_data(self, population_data_path):

        self.data = pd.read_json(population_data_path)
        # Remove prefix 'ZCTA5'
        self.data['NAME'] = self.data['NAME'].map(lambda x: x.lstrip('ZCTA5 '))
        self.data = self.data[['NAME', 'P1_001N']].rename(
            columns={'NAME': 'Zipcode', 'P1_001N': 'Population'})
        self.data["Population"] = self.data["Population"].astype(int)


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

        print("-- Population data data -- ")
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
        self.__adjust_column_names()
        self.__show_statistics()
