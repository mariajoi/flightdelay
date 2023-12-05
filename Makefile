# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr flightdelay-*.dist-info
	@rm -fr flightdelay.egg-info

run_api:
	uvicorn flightdelay.api.fast:app --reload

install:
	@pip install . -U

#################### PACKAGE ACTIONS ###################
ML_DIR=~/flightdelay/mlops

reinstall_package:
	@pip uninstall -y flightdelay || :
	@pip install -e .

run_preprocess:
	python -c 'from flightdelay import ml_logic_preprocessing

run_train:
	python -c 'from flightdelay.interface.main import train; train()'

run_pred:
	python -c 'from flightdelay.interface.main import pred; pred()'

run_all: run_preprocess run_train run_pred run_evaluate

show_sources_all:
	-bq ls ${BQ_DATASET}
	-gsutil ls gs://${BUCKET_NAME}
