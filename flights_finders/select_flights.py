import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd

dotenv_path = Path('env_user.env')
load_dotenv(dotenv_path=dotenv_path)


def select_flights(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a dataframe of flights and a preference (fastest/cheapest) and returns the best
    flights as a dataframe

    Parameters:
    flights_df (pd.DataFrame): Dataframe containing flights per row

    Returns:
    pd.DataFrame: Dataframe with the best flights, if there are multiple flights equally good
                  it contains all those flight options."""

    preference = os.getenv('PREFERENCE')
    best_flights = pd.DataFrame()
    # select flight(s) for both directions
    for direction in ['outward', 'return']:
        if preference == "fastest":
            fastest_single = df[df['direction'] == direction].sort_values(['duration', 'price'])
            # append all flights there are equally good
            best_flights = best_flights.append(df[(df['duration'] == fastest_single[
                                                                        'duration'].iloc[0]) &
                                                  (df['price'] == fastest_single[
                                                                        'price'].iloc[0])])

        elif preference == "cheapest":
            cheapest_single = df[df['direction'] == direction].sort_values(['price', 'duration'])
            # append all flights there are equally good
            best_flights = best_flights.append(df[(df['duration'] == cheapest_single[
                                                                        'duration'].iloc[0]) &
                                                  (df['price'] == cheapest_single[
                                                                        'price'].iloc[0])])
    best_flights['criteria'] = preference
    return best_flights
