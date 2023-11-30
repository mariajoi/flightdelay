from fastapi import FastAPI
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
model = pickle.load(open(f"../pickle/{PICKLE}", "rb"))
app.state.model = load_model(model)   #---- not ready yet put the pickle here

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


    model = app.state.model
    assert model is not None
    y_pred = model.predict(X_pred)   ## set up what is in x by pickle
    return {'wait':y_pred}
