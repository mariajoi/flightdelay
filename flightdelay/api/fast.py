from fastapi import FastAPI
import os
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from flightdelay.data.registry import load_model
import pickle
from flightdelay.utils.mytrans import MyTrans

from flightdelay.ml_logic.params import PICKLE

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define a root `/` endpoint
@app.get("/")
def root():
    return dict(greeting="Hello User, welcome back!")


#Predict the Delay
#direction = os.path.join(os.path.dirname(__file__),"..","data","pickle",PICKLE)
#model = pickle.load(open(f"flightdelay/data/pickle/{PICKLE}", "rb")
app.state.model = load_model()

#coding the load model function

@app.get("/request")
def request(
        airline: str,
        origin: str,
        destination: str,
        departure_time: str,
        arrival_time: str,
        day_of_week: int,
        month:int,
        distance_group:int
    ):


    X_pred = pd.DataFrame({"Operating_Airline": "9E",
                           "Origin": "SHV",
                           "Dest": "ATL",
                           "DepTimeBlk": "1500-1559",
                           "ArrTimeBlk": "1800-1859",
                           "DayOfWork": 4,
                           "Month": 1,
                           "DistanceGroup": 3})
    trans = MyTrans()
    trans.fit(X_pred)
    X_pred_trans = trans.transform(X_pred)

    # When example is done bring it back
    '''
    X_pred = pd.DataFrame({"Operating_Airline": airline,
                           "Origin": origin,"Dest": destination,
                           "DepTimeBlk": departure_time,
                           "ArrTimeBlk": arrival_time,
                           "DayOfWork": day_of_week,
                           "Month": month,
                           "DistanceGroup": distance_group})
    '''


    model = app.state.model
    assert model is not None
    y_pred = model.predict(X_pred_trans)   ## set up what is in x by pickle
    print(y_pred)

    return {'wait':y_pred}
