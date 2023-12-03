import os
import numpy as np
import pickle


##################  VARIABLES  ##################
DATA_SIZE = os.environ.get("DATA_SIZE")
MODEL_TARGET = os.environ.get("MODEL_TARGET")
GCP_PROJECT = os.environ.get("GCP_PROJECT")
GCP_PROJECT_WAGON = os.environ.get("GCP_PROJECT_WAGON")
GCP_REGION = os.environ.get("GCP_REGION")
# BQ_DATASET = os.environ.get("BQ_DATASET")
# BQ_REGION = os.environ.get("BQ_REGION")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
INSTANCE = os.environ.get("INSTANCE")
PICKLE = os.environ.get("PICKLE_NAME")

# GCR_IMAGE = os.environ.get("GCR_IMAGE")
# GCR_REGION = os.environ.get("GCR_REGION")
# GCR_MEMORY = os.environ.get("GCR_MEMORY")

##################  CONSTANTS  #####################
LOCAL_DATA_PATH = '../data/'
# LOCAL_REGISTRY_PATH =  os.path.join(LOCAL_DATA_PATH)

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

################## VALIDATIONS #################

env_valid_options = dict(
    #DATA_SIZE=["1k", "200k", "all"],
    MODEL_TARGET=["local", "gcs", "gci"],
    )

def validate_env_value(env, valid_options):
     env_value = os.environ[env]
     if env_value not in valid_options:
         raise NameError(f"Invalid value for {env} in `.env` file: {env_value} must be in {valid_options}")


for env, valid_options in env_valid_options.items():
     validate_env_value(env, valid_options)
