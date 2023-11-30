# Data analysis
- Project: flightdelay
- Description: Prediction of future flight delay 
- Data Source: Bureau of Transportation Statistics, https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGK&QO_fu146_anzr=b0-gvzr ==> manual download of monthly data for all columns, drawing and concatenating a random sample from each monthly file before running it through the preprocessing pipeline
- Type of analysis: Prediction of flight delay based on certain input factors of the consumer on the interface: Date, origin, destination, time of day for intended flight will predict probability of a delay


# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for flightdelay in github.com/{group}. If your project is not set please add it:

Create a new project on github.com/{group}/flightdelay
Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "flightdelay"
git remote add origin git@github.com:{group}/flightdelay.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
flightdelay-run
```

# Install

Go to `https://github.com/{group}/flightdelay` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/flightdelay.git
cd flightdelay
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
flightdelay-run
```
