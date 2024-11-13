import sqlite3


class DataLoader:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)

    def load_data(self, data, db_name):
        data.to_sql(db_name, self.conn, if_exists='replace')
