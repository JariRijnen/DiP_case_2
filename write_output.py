import pandas as pd
from data_loaders import sql_data


class OutputDb:
    def __init__(self, journey_df):
        self.db_connection = sql_data.connect_postgresql_DB()
        self.conn, self.cur = self.db_connection.return_connection_and_cursor()
        self.journey_df = journey_df
        self.flight_df = pd.DataFrame()

    def write_to_journey_table(self):
        """Takes the best flights df for every employee as input and writes it to SQL tables.
           Returns dataframe including number of flights column"""

        # create number of flights column
        self.journey_df['number_of_flights'] = self.journey_df['stops'].apply(lambda x: len(x)+1)

        query = """INSERT INTO journey (employee_id, criteria, direction, number_of_flights,
                                        duration, price, departure_time, arrival_time, insert_date)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, now())
                ON CONFLICT ON CONSTRAINT unique_journey
                DO NOTHING;"""

        for __, row in self.journey_df[['employee_id', 'criteria', 'direction', 'number_of_flights',
                                        'duration', 'price', 'departure_time',
                                        'arrival_time']].iterrows():
            self.cur.execute(query, list(row))

    def merge_journey_id(self):
        """Takes journey_df, extracts the serial id from the journey sql table and merges journey_df
        with serial id."""

        # extract the unique serial id from journey table and insert into journey_df (only extract
        # the rows of latest hour to merge only the newly added rows)
        journey_id_df = pd.read_sql_query("""SELECT journey_id, employee_id, direction,
                                                      departure_time, arrival_time
                                             FROM journey
                                             WHERE insert_date > (now() - INTERVAL '1 MIN';""",
                                          self.conn)
        self.journey_df = self.journey_df.merge(journey_id_df, how='left', on=['employee_id',
                                                                               'direction',
                                                                               'departure_time',
                                                                               'arrival_time'])

    def create_flights_df(self):
        """Creates a DataFrame for flight per row"""
        self.flight_df = pd.DataFrame(columns=['airline_code', 'flight_number'])

        for __, journey in self.journey_df.iterrows():
            for i, flight in enumerate(journey['all_airports'][:-1]):
                self.flight_df = self.flight_df.append({
                                                'journey_id': journey['journey_id'],
                                                'iata_departure': flight,
                                                'iata_arrival': journey['all_airports'][i+1],
                                                'airline_code': journey['airlines'][i],
                                                'flight_number': i+1},
                                                ignore_index=True)

    def write_to_iata_table(self):
        """add newly seen iata codes to the iata table"""
        query = """INSERT INTO iata (iata_code)
                VALUES(%s)
                ON CONFLICT DO NOTHING;"""
        for iata in self.flight_df['iata_arrival']:
            self.cur.execute(query, [iata])

    def write_to_flight_table(self):
        """add newly seen iata codes to the flight table"""
        query = """INSERT INTO flight (journey_id, iata_departure, iata_arrival, airline_code,
                                    flight_number)
                VALUES(%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;"""
        for __, row in self.flight_df[['journey_id', 'iata_departure', 'iata_arrival',
                                       'airline_code', 'flight_number']].iterrows():
            print(list(row))
            self.cur.execute(query, list(row))

    def write_to_agg_flight_data_table(self):
        """add newly seen iata codes to the write_to_agg_flight_data_table table"""
        query = """INSERT INTO agg_flight_data
                SELECT employee_id,
                        criteria,
                        AVG(price) AS avg_price,
                        MIN(price) AS min_price,
                        AVG(duration) AS avg_duration,
                        MIN(duration) AS min_duration,
                        now() AS insert_date
                FROM journey
                GROUP BY employee_id, criteria;"""
        self.cur.execute(query)

    def write_all_output(self):
        self.write_to_journey_table()
        self.merge_journey_id()
        self.create_flights_df()
        self.write_to_iata_table()
        self.write_to_flight_table()
        self.write_to_agg_flight_data_table()
