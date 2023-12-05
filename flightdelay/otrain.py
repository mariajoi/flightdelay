#General
from colorama import Fore, Style
import pandas as pd
import pickle
import os

#Sklearn
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier
import joblib


#OwnModule
from flightdelay.ml_logic.params import DATA_SIZE,TEST_DATA,TRAIN_DATA, PICKLE_TMP, PICKLE, GCP_PROJECT, BUCKET_NAME
from flightdelay.utils.mytrans import MyTrans
from flightdelay.data.data import COLUMN_NAMES_RAW, COLUMNS_NAMES_DROP

#GCI
from google.cloud import storage




def preproc() -> None:

    print(Fore.MAGENTA + "\n ⭐️ Use case: preprocess" + Style.RESET_ALL)
    base_path = pd.read_csv("/data/")
    trans = MyTrans()

    ## upload csv from Cloud

    file_path_test = os.path.join(base_path,TEST_DATA)
    file_path_train = os.path.join(base_path,TRAIN_DATA)
    X_test = pd.read_csv(file_path_test, usecols=COLUMN_NAMES_RAW).drop("Unnamed: 0",axis=1).drop(columns=COLUMNS_NAMES_DROP)
    X_train = pd.read_csv(file_path_train, usecols=COLUMN_NAMES_RAW).drop("Unnamed: 0",axis=1).drop(columns=COLUMNS_NAMES_DROP)
    data_X = [X_test,X_train]
    y_train = []
    y_test = []
    X_train_trans = []
    X_test_trans = []

    if X_train.shape[0] < 10:
        print("❌ Not enough processed data retrieved to train on")
        return None

    for sample in data_X:
        sample["BadFlight"] = ((sample['ArrivalDelayGroups'] > 0) | (sample['Cancelled'] > 0)).astype(int)

        # Erstelle die Zielvariable y
        y = sample["BadFlight"]
        trans.fit(sample)


        if "train" in data_X:
            y_train.append(y)
            X_train_trans = trans.transform(X_train)
        elif "test" in data_X:
            y_test.append(y)
            X_test_trans = trans.transform(X_test)

    return y_train,y_test,X_test_trans,X_train_trans

'''
def load_empty_model() -> None:
    # Load template pipeline from pickle file
    preproc_pipe = pickle.load(open("../pickle/"&PICKLE_TMP, "rb"))
    return preproc_pipe

'''

# TRAIN AND LOAD MODEL SECTION
client = storage.Client(project=GCP_PROJECT)
bucket = client.bucket(BUCKET_NAME)
gcs_path = f"gs://{BUCKET_NAME}/{PICKLE_TMP}" #CHange Pickle if needed

def load_trained_model():
    # Load pipeline from pickle file
    #pipeline = pickle.load(open(f"/pickle/{PICKLE_TMP}","rb")) --> local solution
    model_load = joblib.load(gcs_path)
    return model_load

def cross_val():
    pipeline = load_trained_model()
    y_train,y_test,X_test_trans,X_train_trans = preproc()
    score = cross_val_score(pipeline, X_train_trans, y_train, cv=5, scoring='recall').mean()
    print(score)
    return score

def train_model():
    pipeline = load_trained_model()

    # Add Params of model
    model = RandomForestClassifier(max_depth=5,class_weight="balanced", random_state=42)
    y_train,y_test,X_test_trans,X_train_trans = preproc()

    #model = load_model()
    #assert model is not None         < --- take this part and delete RandomForest

    # Create and Fit Pipeline
    model_pipeline = make_pipeline(pipeline, model)
    model_pipeline.fit(X_train_trans,y_train)
    pipeline.fit(X_train_trans,y_train)
    result = pipeline
    return result

def predict():
    y_train,y_test,X_test_trans,X_train_trans = preproc()
    model = train_model()
    guess = model.predict(X_test_trans[1])   # test with second row
    return guess

# Save a model online on
def save_model(name):
    storage_filename = f"{name}"
    model = train_model()

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(storage_filename)
    blob.upload_from_filename(model)
    return print("Upload done")


'''
if __name__ == '__main__':
    preproc()
'''
