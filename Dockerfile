FROM python:3.10.6-buster


WORKDIR /prod


RUN python -m pip install --upgrade pip setuptools
RUN pip install --upgrade pip

COPY requirements_prod.txt requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt
#RUN pip install -r requirements.txt


COPY flightdelay flightdelay
COPY setup.py setup.py
RUN pip install .




# dont forget docker run api -p XXXXX - 8000

CMD uvicorn flightdelay.api.fast:app --host 0.0.0.0 --port $PORT
