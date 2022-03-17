import pandas as pd
import time

from data_loaders import api_data, sql_data
from travel_days import travel_days
from flights_finders import available_flights, select_flights
from base_logger import logger
import write_output


def main():

    home_airports = ['AMS', 'EIN']

    employee_db = sql_data.connect_postgresql_DB()
    dip_df = employee_db.insert_sql_data()
    dip_df = dip_df.head(20)
    amadeus_db = api_data.Amadeus_DB()

    deperature_day, return_day = travel_days()

    return_df = pd.DataFrame()
    for __, row in dip_df.iterrows():
        print(row['employee_id'])
        try:
            flights_df = pd.DataFrame()
            # Find all available flights for all home airports.
            for home_airport in home_airports:
                amadeus_data = amadeus_db.insert_flight_data(departure_airport=home_airport,
                                                             destination=row['iata_code'],
                                                             deperature_day=deperature_day,
                                                             return_day=return_day)
                flights_data = available_flights(amadeus_data, row['employee_id'])
                flights_df = flights_df.append(flights_data)

            # Select only the best flights that match the preference
            best_flights = select_flights(flights_df)
            print(best_flights)

            return_df = return_df.append(best_flights)

        # Log the occasions where there is no IATA code given and a KeyError is raised.
        except KeyError:
            logger.info(f" {row['employee_id']} has no correct IATA code present")
        except IndexError:
            logger.info(f" {row['employee_id']} has no available flights")
        time.sleep(0.5)

    # Write final dataframe to SQL tables
    output_writer = write_output.output_writer(return_df)
    output_writer.write_all_output()


if __name__ == '__main__':
    main()
