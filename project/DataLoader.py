import os
import sqlite3


class DataLoader:
    def __init__(self, path):
        self.path = path

    def load_data(self, data, db_name):
        # Delete already existing db
        try:
            os.remove(self.path)
        except OSError:
            pass

        conn = sqlite3.connect(self.path)
        data.to_sql(db_name, conn, if_exists='replace')
        print('Data loaded to ', self.path)
