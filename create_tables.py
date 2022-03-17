from data_loaders import sql_data


def drop_tables():
    """Drops tables and ENUM's if they exist"""

    cur.execute("DROP TABLE IF EXISTS city CASCADE")
    cur.execute("DROP TABLE IF EXISTS country CASCADE")
    cur.execute("DROP TABLE IF EXISTS iata CASCADE")
    cur.execute("DROP TABLE IF EXISTS flight CASCADE")
    cur.execute("DROP TABLE IF EXISTS employee CASCADE")
    cur.execute("DROP TABLE IF EXISTS journey CASCADE")
    cur.execute("DROP TABLE IF EXISTS covid_info CASCADE")
    cur.execute("DROP TABLE IF EXISTS agg_flight_data CASCADE")

    cur.execute("DROP TYPE IF EXISTS preference CASCADE")
    cur.execute("DROP TYPE IF EXISTS risk_level CASCADE")
    cur.execute("DROP TYPE IF EXISTS direction CASCADE")


def create_tables():
    """Creates tables in the postgresql database. (First deletes those tables if they exist)"""

    with open('sql\CREATE_country.sql') as f:
        cur.execute(f.read())

    with open('sql\CREATE_covid_info.sql') as f:
        cur.execute(f.read())

    with open('sql\CREATE_city.sql') as f:
        cur.execute(f.read())

    with open('sql\CREATE_iata.sql') as f:
        cur.execute(f.read())

    with open('sql\CREATE_employee.sql') as f:
        cur.execute(f.read())

    with open('sql\CREATE_journey.sql') as f:
        cur.execute(f.read())

    with open('sql\CREATE_flight.sql') as f:
        cur.execute(f.read())

    with open('sql\CREATE_agg_flight_data.sql') as f:
        cur.execute(f.read())


if __name__ == '__main__':
    db_connection = sql_data.connect_postgresql_DB()
    conn, cur = db_connection.return_connection_and_cursor()

    drop_tables()
    create_tables()
