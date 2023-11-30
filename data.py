import pandas as pd
import os

from flightdelay.ml_logic.params import COLUMN_NAMES_RAW


def clean_data():
    base_path = 'flightdelay/raw_data/'

    num_files = len(os.listdir(base_path))
    current_db_final = pd.DataFrame()
    list_of_dfs = []


    for i in range(1, num_files + 2):
        file_name = f'On_Time_Marketing_Carrier_On_Time_Performance_(Beginning_January_2018)_2022_{i}.csv'
        file_path = os.path.join(base_path, file_name)

        if os.path.exists(file_path):
            current_db_aktuell = pd.read_csv(file_path, usecols=COLUMN_NAMES_RAW).sample(n=1000, random_state=42)

            int_columns = current_db_aktuell.select_dtypes(include='int64').columns
            current_db_aktuell[int_columns] = current_db_aktuell[int_columns].astype('int16')
            float_columns = current_db_aktuell.select_dtypes(include='float64').columns
            current_db_aktuell[float_columns] = current_db_aktuell[float_columns].astype('float16')

            current_db_aktuell['selection'] = (current_db_aktuell['ArrDel15'] + current_db_aktuell['Cancelled'])
            selection_counts = current_db_aktuell['selection'].value_counts()
            num_samples_to_drop = selection_counts[0] - selection_counts[1]

            if num_samples_to_drop > 0:
                df_to_drop = current_db_aktuell[current_db_aktuell['selection'] == 0].sample(n=num_samples_to_drop, random_state=42)
                current_db_aktuell = current_db_aktuell.drop(df_to_drop.index)

            current_db_aktuell.drop(columns='selection', inplace=True)
            list_of_dfs.append(current_db_aktuell)

            current_db_final = pd.concat([current_db_final, current_db_aktuell])

    current_db_final.rename(columns={current_db_final.columns[4]: "Operating_Airline"}, inplace=True)

    print("✅ Data cleaned")

    current_db_final.to_csv('5k_zeros_removed.csv')

clean_data()
