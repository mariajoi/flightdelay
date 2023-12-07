import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

main_file = os.path.join(script_dir, '..', 'data', 'lookup.csv')
carrier_codes = os.path.join(script_dir, '..', 'data', 'carrier codes.csv')

df = pd.read_csv(main_file)
carrier_codes = pd.read_csv(carrier_codes)

df = pd.merge(df, carrier_codes, left_on='Operating_Airline', right_on='airline', how='left')

available_options = {}
distance_groups = {}

for index, row in df.iterrows():
    origin = row['Origin']
    origincityname = row['OriginCityName']
    destination = row['Dest']
    destcityname = row['DestCityName']
    airline = row['name']
    distance_group = row['DistanceGroup']

    if origincityname not in available_options:
        available_options[origincityname] = {destcityname: [airline]}
    else:
        if destcityname not in available_options[origincityname]:
            available_options[origincityname][destcityname] = [airline]
        else:
            if airline not in available_options[origincityname][destcityname]:
                available_options[origincityname][destcityname].append(airline)

    distance_groups[(origin, destination)] = distance_group

def get_available_options():
    return available_options

def get_distance_groups(origin, destination):
    return distance_groups.get((origin, destination), None)

def get_airport_code(city_name):
    city_to_airport = dict(zip(df['OriginCityName'], df['Origin']))
    return city_to_airport.get(city_name, None)

def get_airline_code(airline_name):
    airline_to_code = dict(zip(df['name'], df['Operating_Airline']))
    return airline_to_code.get(airline_name, None)
