import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
import urllib.parse

dotenv_path = Path('env_user.env')
load_dotenv(dotenv_path=dotenv_path)


class PostgresDb:
    def __init__(self):
        self.username = os.getenv('DB_USERNAME')
        self.password = urllib.parse.quote(os.getenv('DB_PASSWORD'))
        self.host_name = os.getenv('DB_HOST_NAME')
        self.name = os.getenv('DB2_NAME')

    def return_connection_and_cursor(self):
        """Establishes a connection to the postgresql database and returns the connection
           and cursor"""

        conn = psycopg2.connect("postgresql://{}:{}@{}/{}".format(self.username,
                                                                  self.password,
                                                                  self.host_name,
                                                                  self.name))
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        return conn, cur

    def get_employee_data(self) -> pd.DataFrame:
        """Gets SQL employee data from database and puts that into a pandas dataframe"""

        with self.return_connection_and_cursor()[0] as con:
            query = """SELECT e.employee_id, i.iata_code
                       FROM employee e
                       JOIN iata i
                       ON (e.iata_code = i.iata_code);"""
            df = pd.read_sql(query, con)

            return df


if __name__ == '__main__':
    dip_data = PostgresDb()
    df = dip_data.get_employee_data()()
    print(df.dtypes)
    print(df.head(5))
