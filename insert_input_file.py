import pandas as pd
import airportsdata
import time

from data_loaders import sql_data, api_data


def insert_input_file(path):
    """
    Takes a csv file containing employee and flight preference data as input, loads it as a
    dataframe. Retrieves information from airportsdata to find the corresponding city name and
    country code per IATA code. Then retrieves information from the Amadeus API concerning
    covid information.

    Enters all this data into an SQL employee, iata, city, country code and covid info table.

    Parameters:
    path (str): Path to CSV file.
    """
    input_df = pd.read_csv(path, sep=";", names=['first_name', 'last_name',
                                                 'city', 'iata_code'])
    input_df.drop('city', axis=1, inplace=True)
    input_df['iata_code'] = input_df['iata_code'].apply(lambda x: x.upper())

    # find city and country bases on IATA code, return None if not available
    airports = airportsdata.load('IATA')
    input_df['city_name'] = input_df['iata_code'].apply(lambda x: airports.get(x)['city'] if
                                                        airports.get(x) is not None else None)
    input_df['country_code'] = input_df['iata_code'].apply(lambda x: airports.get(x)['country'] if
                                                           airports.get(x) is not None else None)

    input_df = input_df.assign(city_id=(input_df['city_name'].astype('category')).cat.codes)

    return input_df


def get_covid_info(df: pd.DataFrame) -> pd.DataFrame:
    """Calls amadeus endpoint API to get covid travel information

    Parameters:
    df: dataframe of employee, city, iata and country

    Returns:
    pd.DataFrame: dataframe with covid information added.
    """

    amadeus_db = api_data.Amadeus_DB()
    for i, row in df.iterrows():
        covid_dict = amadeus_db.insert_covid_country_data(row['country_code'])
        # print(row['country_code'], covid_dict)
        df.loc[i, 'country_name'] = covid_dict['country']
        df.loc[i, 'risk_level'] = covid_dict['risk_level']
        df.loc[i, 'fully_vaccinated'] = covid_dict['vaccination_rate']
        df.loc[i, 'test_required'] = covid_dict['test_required']
        df.loc[i, 'vaccination_required'] = covid_dict['vaccination_required']
        time.sleep(1)

    return df


def insert_into_sql(df: pd.DataFrame):
    """Inserts df of all gathered input data in SQl tables.

    Parameters:
    df: input dataframe of with emplyee, city, iata, country and covid data
    """

    query = """INSERT INTO country (country_code, country_name)
            VALUES(%s, %s)
            ON CONFLICT DO NOTHING;"""
    for i, row in df[['country_code', 'country_name']].drop_duplicates().iterrows():
        cur.execute(query, list(row))

    query = """INSERT INTO city (city_id, city_name, country_code)
            VALUES(%s, %s, %s)
            ON CONFLICT DO NOTHING;"""
    for i, row in df[['city_id', 'city_name', 'country_code']].drop_duplicates().iterrows():
        cur.execute(query, list(row))

    query = """INSERT INTO iata (iata_code, city_id)
            VALUES(%s, %s)
            ON CONFLICT DO NOTHING;"""
    for i, row in df[['iata_code', 'city_id']].drop_duplicates().iterrows():
        cur.execute(query, list(row))

    query = """INSERT INTO employee (first_name, last_name, iata_code)
            VALUES(%s, %s, %s)
            ON CONFLICT DO NOTHING;"""
    for i, row in df[['first_name', 'last_name', 'iata_code']].drop_duplicates().iterrows():
        cur.execute(query, list(row))

    query = """INSERT INTO covid_info (country_code, fully_vaccinated, test_required,
            vaccination_required, risk_level, insert_date)
            VALUES(%s, %s, %s, %s, %s, now())
            ON CONFLICT DO NOTHING;"""
    for i, row in df[['country_code', 'fully_vaccinated', 'test_required',
                      'vaccination_required', 'risk_level']].drop_duplicates().iterrows():
        cur.execute(query, list(row))


if __name__ == '__main__':
    db_connection = sql_data.connect_postgresql_DB()
    conn, cur = db_connection.return_connection_and_cursor()

    df = insert_input_file('data/input_file.csv')

    input_df = get_covid_info(df)

    insert_into_sql(input_df)
