#General
from colorama import Fore, Style
import pandas as pd
import pickle
import os

#Sklearn
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, f1_score, precision_score
import joblib


#OwnModule
from flightdelay.ml_logic.params import DATA_SIZE,TEST_DATA,TRAIN_DATA, PICKLE_TMP, PICKLE, GCP_PROJECT, BUCKET_NAME, COLUMN_NAMES
from flightdelay.utils.mytrans import MyTrans
from flightdelay.data.data import COLUMN_NAMES_RAW, COLUMNS_NAMES_DROP
#GCI
from google.cloud import storage




def preproc():

    print(Fore.MAGENTA + "\n ⭐️ Use case: preprocess" + Style.RESET_ALL)
    base_path = os.path.join(os.path.dirname(__file__), 'data/')
    trans = MyTrans()

    ## upload csv from Cloud
    # .drop("Unnamed: 0",axis=1) not on VS just Jupyter

    file_path_test = os.path.join(base_path,TEST_DATA)
    file_path_train = os.path.join(base_path,TRAIN_DATA)
    X_test = pd.read_csv(file_path_test, usecols=COLUMN_NAMES)
    X_train = pd.read_csv(file_path_train, usecols=COLUMN_NAMES)
    data_X = [X_test,X_train]
    y_train = []
    y_test = []
    X_train_trans = []
    X_test_trans = []

    if X_train.shape[0] < 10:
        print("❌ Not enough processed data retrieved to train on")
        return None

    for sample,title in zip(data_X,['test','train']):
        sample["BadFlight"] = ((sample['ArrivalDelayGroups'] > 0) | (sample['Cancelled'] > 0)).astype(int)

        # Erstelle die Zielvariable y
        y = sample["BadFlight"]
        trans.fit(sample)


        if title == 'train':
            y_train.append(y)
            X_train_trans = trans.transform(X_train).drop(columns=COLUMNS_NAMES_DROP)
        elif title == 'test':
            y_test.append(y)
            X_test_trans = trans.transform(X_test).drop(columns=COLUMNS_NAMES_DROP)

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

def train_model_rand():
    pipeline = load_trained_model()

    # Add Params of model
    y_train,y_test,X_test_trans,X_train_trans = preproc()


    # Create and Fit Pipeline

    randomF = RandomForestClassifier(class_weight='balanced', random_state=42)

    model_pipeline = make_pipeline(pipeline, randomF)
    model_pipeline.fit(X_train_trans,y_train)

    y_preds_tr = model_pipeline.predict(X_train_trans)
    y_preds = model_pipeline.predict(X_test_trans)

    print('Train data scores:')
    print('accuracy: %.3f' % accuracy_score(y_preds_tr,y_train))
    print('f1_score: %.3f' % f1_score(y_preds_tr,y_train, average='binary'))
    print('recall: %.3f' % recall_score(y_preds_tr,y_train,average='binary'))
    print('precision: %.3f' % precision_score(y_preds_tr,y_train,average='binary'))
    print("Confusion Matrix: ", confusion_matrix(y_preds_tr,y_train))

    print('Test data scores:')
    print('accuracy: %.3f' % accuracy_score(y_preds,y_test))
    print('f1_score: %.3f' % f1_score(y_preds, y_test, average='binary'))
    print('recall: %.3f' % recall_score(y_preds, y_test,average='binary'))
    print('precision: %.3f' % precision_score(y_preds, y_test,average='binary'))
    print("Confusion Matrix: ", confusion_matrix(y_preds,y_test))

    #model = load_model()
    #assert model is not None         < --- take this part and delete RandomForest


    return model_pipeline

def predict_model():
    y_train,y_test,X_test_trans,X_train_trans = preproc()
    model = train_model_rand()
    guess = model.predict(X_test_trans[1])   # test with second row
    return guess

# Save a model online on
def save_model(name):
    storage_filename = f"{name}"
    model = train_model_rand()

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(storage_filename)
    blob.upload_from_filename(model)
    return print("Upload done")



if __name__ == '__main__':
    preproc()
    load_trained_model()
    cross_val()
    train_model_rand()
