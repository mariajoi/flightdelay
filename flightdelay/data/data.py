import pandas as pd
import os
import pickle


COLUMN_NAMES_RAW = ['Month', 'DayofMonth', 'DayOfWeek', 'FlightDate',
       'Operating_Airline ', 'Tail_Number', 'Flight_Number_Operating_Airline',
       'OriginAirportID', 'Origin', 'OriginCityName', 'OriginState',
       'DestAirportID', 'Dest', 'DestCityName', 'DestState', 'CRSDepTime',
       'DepTime', 'DepDelay', 'DepDelayMinutes', 'DepDel15',
       'DepartureDelayGroups', 'DepTimeBlk', 'CRSArrTime', 'ArrTime',
       'ArrDelay', 'ArrDelayMinutes', 'ArrDel15', 'ArrivalDelayGroups',
       'ArrTimeBlk', 'Cancelled', 'CancellationCode', 'Diverted',
       'CRSElapsedTime', 'ActualElapsedTime', 'AirTime', 'Distance',
       'DistanceGroup', 'CarrierDelay', 'WeatherDelay', 'NASDelay',
       'SecurityDelay', 'LateAircraftDelay']

def clean_data():
    base_path = '../raw_data/'

    current_db_final = pd.DataFrame()
    test_samples = []

    for file_name in os.listdir(base_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(base_path, file_name)
            df = pd.read_csv(file_path, usecols=COLUMN_NAMES_RAW).sample(n=1300, random_state=42)

            test_sample = df.sample(n=300, random_state=42)
            train_sample = df.drop(test_sample.index)

            int_columns = train_sample.select_dtypes(include='int64').columns
            train_sample[int_columns] = train_sample[int_columns].astype('int16')
            float_columns = train_sample.select_dtypes(include='float64').columns
            train_sample[float_columns] = train_sample[float_columns].astype('float16')

            train_sample['selection'] = (train_sample['ArrDel15'] + train_sample['Cancelled'])
            selection_counts = train_sample['selection'].value_counts()
            num_samples_to_drop = selection_counts[0] - selection_counts[1]

            if num_samples_to_drop > 0:
                df_to_drop = train_sample[train_sample['selection'] == 0].sample(n=num_samples_to_drop, random_state=42)
                train_sample = train_sample.drop(df_to_drop.index)

            current_db_final = pd.concat([current_db_final, train_sample])

            test_samples.append(test_sample)

            current_db_final = pd.concat([current_db_final, train_sample])

    current_db_final.drop(columns=['selection'], inplace=True) 
    current_db_final.rename(columns={current_db_final.columns[4]: "Operating_Airline"}, inplace=True)

    print("✅ Data cleaned")

    train_sample = pd.concat(test_samples)
    test_sample = pd.concat(test_samples)

    current_db_final.to_csv('train_sample.csv')  # Save the concatenated data as train_sample.csv
    test_sample.to_csv('test_sample.csv')  # Save test_sample.csv

clean_data()

def get_pickle():
    # Load pipeline from pickle file
    my_pipeline = pickle.load(open("../03-Tuning-Pipeline/pipeline.pkl", "rb"))
