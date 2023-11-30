FROM python:3.10.6-buster

COPY requirements_prod.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install --upgrade pip

#COPY flightdelay flightdelay    - not yet done
#RUN pip install .

# dont forget docker run api -p XXXXX - 8000

CMD uvicorn flightdelay.api.fast:app --host 0.0.0.0 --port $PORT
