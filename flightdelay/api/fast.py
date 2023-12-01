from fastapi import FastAPI
import os
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
# from flightdelay.data.registry import load_model
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

# YOU need flightdelay git:(master) uvicorn flightdelay.api.fast:app --reload to test it
# Define a root `/` endpoint
# @app.get("/")
# def root():
#     return dict(greeting="Hello User, welcome back!")

#Predict the Delay
#direction = os.path.join(os.path.dirname(__file__).replace("/api",""), "pickle", PICKLE)
relative_path = os.path.join(os.path.dirname(__file__), "..", "pickle", PICKLE)
#model = pickle.load(open(relative_path, "rb"))
#app.state.model = load_model()

with open(relative_path, 'rb') as file:
    loaded_model = pickle.load(file)

app.state.model = loaded_model

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

    '''
    X_pred = pd.DataFrame({"Operating_Airline": "9E",
                           "Origin": "SHV",
                           "Dest": "ATL",
                           "DepTimeBlk": "1500-1559",
                           "ArrTimeBlk": "1800-1859",
                           "DayOfWeek": 4,
                           "Month": 1,
                           "DistanceGroup": 3})
    '''


    # When example is done bring it back

    X_pred = pd.DataFrame({"Operating_Airline": airline,
                           "Origin": origin,
                           "Dest": destination,
                           "DepTimeBlk": departure_time,
                           "ArrTimeBlk": arrival_time,
                           "DayOfWeek": day_of_week,
                           "Month": month,
                           "DistanceGroup": distance_group}, index = [0])

    trans = MyTrans()
    trans.fit(X_pred)
    X_pred_trans = trans.transform(X_pred)

    model = app.state.model
    assert model is not None
    y_pred = model.predict(X_pred_trans)[0]   ## set up what is in x by pickle
    #result = loaded_model.predict(X_pred_trans)

    #return {'wait':y_pred}
    return dict(result=str(y_pred))
    #ValueError: If using all scalar values, you must pass an index
