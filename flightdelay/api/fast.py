from fastapi import FastAPI
import os
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from flightdelay.data.registry import load_model
import pickle

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
        departure_bracket: str,
        arrival_bracket: str,
        day_of_week: int,
        month_number:int
    ):

    new_data = pd.read_csv("https://wagon-public-datasets.s3.amazonaws.com/05-Machine-Learning/08-Workflow/pickle_pipe_data.csv")
    new_data

    X_pred = new_data
    #X_pred = dict({"airline":airline,"origin":origin,"destination":destination,"departure_bracket":departure_bracket,"arrival_bracket":arrival_bracket,"day_of_week":day_of_week,"month_number":month_number})
    model = app.state.model
    assert model is not None
    y_pred = model.predict(X_pred)   ## set up what is in x by pickle
    return {'wait':y_pred}
