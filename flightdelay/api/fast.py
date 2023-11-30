from fastapi import FastAPI
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import pickle 

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
model = pickle.load(open("../03-Tuning-Pipeline/pipeline.pkl", "rb"))
app.state.model = load_model(model)   ---- not ready yet put the pickle here 

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


    model = app.state.model   ---- not ready yet
    #assert model is not None ---- not ready yet
    #y_pred = model.predict(X_processed) --- not ready yet
    return {'wait':64}
