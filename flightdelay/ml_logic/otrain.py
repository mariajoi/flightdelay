from colorama import Fore, Style
from utils.mytrans import MyTrans
import pandas as pd
import pickle
import os
from flightdelay.ml_logic.params import DATA_SIZE,TEST_DATA,TRAIN_DATA
from flightdelay.data.data import COLUMN_NAMES_RAW

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
    base_path = pd.read_csv("../data/")

    file_path_test = os.path.join(base_path,TRAIN_DATA)
    file_path_train = os.path.join(base_path,TRAIN_DATA)
    df_test = pd.read_csv(file_path_test, usecols=COLUMN_NAMES_RAW).drop("Unnamed: 0",axis=1)
    df_train = pd.read_csv(file_path_train, usecols=COLUMN_NAMES_RAW).drop("Unnamed: 0",axis=1)
    data_df = [df_test,df_train]
    y_train = []
    y_test = []

    for sample in data_df:
        sample["BadFlight"] = ((sample['ArrivalDelayGroups'] > 0) | (sample['Cancelled'] > 0)).astype(int)
        # Erstelle die Zielvariable y
        y = sample["BadFlight"]

    if "train" in data_df:
        y_train.append(y)
    elif "test" in df_name:
        y_test.append(y)

    if df_train.shape[0] < 10:
        print("❌ Not enough processed data retrieved to train on")
        return None

'''
if __name__ == '__main__':
    preproc()
'''
