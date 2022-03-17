import pandas as pd


def available_flights(amadeus_data: list of json type lists, employee_id: str) -> pd.DataFrame:
    """
    Takes a json list as input and returns a dataframe with available retourflights.

    Parameters:
    amadeus_data (list): Contains two lists, the first for outward flights, the second for
                         return flights. Both lists contain json type lists.
    employee_id (int): Id number of the employee

    Returns:
    pd.DataFrame: Dataframe containing a single flight and related information per row.
    """

    df = pd.DataFrame(columns=('employee_id', 'direction', 'iata_departure_airport',
                               'iata_arrival_airport', 'price', 'departure_time',
                               'arrival_time', 'duration', 'stops', 'airlines'))

    # use both flight directions
    for k, direction in enumerate(['outward', 'return']):
        # iterate over every flight within the direction list
        for data_entry in amadeus_data[k]:
            iata_departure_airport = data_entry['itineraries'][0]['segments'][0]['departure'][
                'iataCode']
            # strip time from irrelevant characters
            departure_time = data_entry['itineraries'][0]['segments'][0][
                                                'departure']['at'].replace('T', ' ')
            iata_arrival_airport = data_entry['itineraries'][0]['segments'][-1]['arrival'][
                'iataCode']
            arrival_time = data_entry['itineraries'][0]['segments'][-1][
                                            'arrival']['at'].replace('T', ' ')
            time = data_entry['itineraries'][0]['duration']
            mins = ':0' if time[-3:-2] == 'H' else (':00:00' if time[-1] == 'H' else ':')
            duration = time.replace('H', mins).replace('M', ':00')[2:]

            price = float(data_entry['price']['total'])
            airlines = [
                data_entry['itineraries'][0]['segments'][j]['carrierCode'] for j in range(
                    0, len(data_entry['itineraries'][0]['segments']))]
            stops = [data_entry['itineraries'][0]['segments'][j][
                'arrival']['iataCode'] for j in range(
                    0, len(data_entry['itineraries'][0]['segments'])-1)]

            # append all flight data into a new row for the return dataframe
            df = df.append({'employee_id': employee_id, 'direction': direction,
                            'iata_departure_airport': iata_departure_airport,
                            'iata_arrival_airport': iata_arrival_airport, 'price': price,
                            'departure_time': departure_time,
                            'arrival_time': arrival_time, 'duration': duration,
                            'stops': stops, 'airlines': airlines},
                           ignore_index=True)
            df['duration'] = pd.to_timedelta(df['duration'])
            df[['departure_time', 'arrival_time']] = df[['departure_time',
                                                         'arrival_time']].apply(pd.to_datetime)
            df['all_airports'] = df['iata_departure_airport'].apply(lambda x: [x]) + df[
                                    'stops'] + df['iata_arrival_airport'].apply(lambda x: [x])

    return df
