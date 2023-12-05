#General
from colorama import Fore, Style
import pandas as pd
import pickle
import os

#Sklearn
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier

#OwnModule
from flightdelay.ml_logic.params import DATA_SIZE,TEST_DATA,TRAIN_DATA, PICKLE_TMP, PICKLE, GCP_PROJECT, BUCKET_NAME
from flightdelay.utils.mytrans import MyTrans
from flightdelay.data.data import COLUMN_NAMES_RAW, COLUMNS_NAMES_DROP

#GCI
from google.cloud import storage


'''

#### from the train chal
def preprocess() -> None:

    print(Fore.MAGENTA + "\n ⭐️ Use case: preprocess" + Style.RESET_ALL)

    if data_processed.shape[0] < 10:
        print("❌ Not enough processed data retrieved to train on")
        return None



    model = load_model()
    assert model is not None

    X_processed = preprocess_features(X_pred)
    y_pred = model.predict(X_processed)

    print("\n✅ prediction done: ", y_pred, y_pred.shape, "\n")
    return y_pred



    train(min_date='2009-01-01', max_date='2015-01-01')
    evaluate(min_date='2009-01-01', max_date='2015-01-01')
    pred()

'''



def preproc() -> None:

    print(Fore.MAGENTA + "\n ⭐️ Use case: preprocess" + Style.RESET_ALL)
    base_path = pd.read_csv("/data/")
    trans = MyTrans()

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
client = storage.Client(project=GCP_PROJECT)
local_path = 'temp_model.pkl'
bucket_name = BUCKET_NAME

def load_trained_model():
    # Load pipeline from pickle file
    pipeline = pickle.load(open(f"/pickle/{PICKLE_TMP}rb"))
    return pipeline

def cross_val():
    pipeline = load_trained_model()
    y_train,y_test,X_test_trans,X_train_trans = preproc()
    score = cross_val_score(pipeline, X_train_trans, y_train, cv=5, scoring='recall').mean()
    print(score)
    return score

def train_model():
    pipeline = load_trained_model()

    # Add Params of model
    model = RandomForestClassifier(max_depth=5, random_state=42)
    y_train,y_test,X_test_trans,X_train_trans = preproc()

    #model = load_model()
    #assert model is not None         < --- take this part and delete RandomForest

    # Create and Fit Pipeline
    model_pipeline = make_pipeline(pipeline, model)
    model_pipeline.fit(X_train_trans,y_train)
    pipeline.fit(X_train_trans,y_train)
    result = pipeline
    return result

def predict(X):
    model = train_model()
    guess = model.predict(X)
    return guess

def save_model(name):
    gci_path = f"{GCP_PROJECT}/preproc_nottrans_notfit_.pkl"{}
    model = train_model()
    model


'''
if __name__ == '__main__':
    preproc()
'''
