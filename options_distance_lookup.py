import pandas as pd

df = pd.read_csv('base_data_all.csv')

available_options = {}
distance_groups = {}

for index, row in df.iterrows():
    origin = row['Origin']
    destination = row['Dest']
    airline = row['Operating_Airline']
    distance_group = row['DistanceGroup']

    if origin not in available_options:
        available_options[origin] = {destination: [airline]}
    else:
        if destination not in available_options[origin]:
            available_options[origin][destination] = [airline]
        else:
            if airline not in available_options[origin][destination]:
                available_options[origin][destination].append(airline)

    distance_groups[(origin, destination)] = distance_group

def get_available_options():
    return available_options

def get_distance_groups(origin, destination):
    return distance_groups.get((origin, destination), None)

print(get_distance_groups('JFK','LAX'))
