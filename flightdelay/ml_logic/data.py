import pandas as pd
import os
from google.cloud import bigquery
from colorama import Fore, Style
from pathlib import Path

from flightdelay.ml_logic.params import COLUMN_NAMES_RAW


def clean_data():
    base_path = 'flightdelay/raw_data/'

    num_files = len(os.listdir(base_path))
    current_db_final = pd.DataFrame()

    for i in range(1, num_files + 2):
        file_name = f'On_Time_Marketing_Carrier_On_Time_Performance_(Beginning_January_2018)_2022_{i}.csv'
        file_path = os.path.join(base_path, file_name)

        if os.path.exists(file_path):
            current_db_aktuell = pd.read_csv(file_path, usecols=COLUMN_NAMES_RAW).sample(n=2000, random_state=42)
            current_db_aktuell.select_dtypes(include='int64').astype('int16')
            current_db_aktuell.select_dtypes(include='float64').astype('float16')

            current_db_final = pd.concat([current_db_final, current_db_aktuell])

    current_db_final.rename(columns={current_db_final.columns[4]: "Operating_Airline"}, inplace=True)

    print("✅ Data cleaned")

    current_db_final.to_csv('base_data_all.csv')

# def load_data_to_bq(
#         data: pd.DataFrame,
#         gcp_project:str,
#         bq_dataset:str,
#         table: str,
#         truncate: bool
#     ) -> None:
#     data = 'base_data.csv'
#     assert isinstance(data, pd.DataFrame)
#     full_table_name = f"{gcp_project}.{bq_dataset}.{table}"
#     print(Fore.BLUE + f"\nSave data to BigQuery @ {full_table_name}...:" + Style.RESET_ALL)

#     # Load data onto full_table_name

#     data.columns = [f"_{column}" if not str(column)[0].isalpha() and not str(column)[0] == "_" else str(column) for column in data.columns]

#     client = bigquery.Client()

#     # Define write mode and schema
#     write_mode = "WRITE_TRUNCATE" if truncate else "WRITE_APPEND"
#     job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

#     print(f"\n{'Write' if truncate else 'Append'} {full_table_name} ({data.shape[0]} rows)")

#     # Load data
#     job = client.load_table_from_dataframe(data, full_table_name, job_config=job_config)
#     result = job.result()  # wait for the job to complete

#     print(f"✅ Data saved to bigquery, with shape {data.shape}")

clean_data()
