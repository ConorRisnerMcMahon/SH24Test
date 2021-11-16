# Postcode search app

An application to search for a UK postcode and find out whether or not that postcode is within the service area.

A postcode is defined as with the service area if either:
1. The postcode has been explicitly listed as servable
2. The postcode’s LSOA code starts with any string explicitly listed as an allowed LSOA-code-start

The configuration for servable postcodes and LSOAs-beginnings are found at `/app/data/allowed_postcodes.json` and `/app/data/allowed_local_authorities.json`


## Setting up the app for development

1. Install [pyenv](https://github.com/pyenv/pyenv#installation) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv#installation)
2. Initialise a python 3.9.1 virtual environment: `pyenv virtualenv 3.9.1 postcode_checker`
3. Activate the virtual environment `pyenv activate postcode_checker`
3. Install the project requirements: `pip install -r requirements.txt`


## Running the app locally

From the project root, run the app with `flask run`


## Running the tests

- To run the unit tests: `./scripts/run_unit_tests.sh`
- To run the integration tests: `./scripts/run_integration_tests.sh`
- To run the end to end tests: `./scripts/run_end_to_end_tests.sh`
- To run the entire test suit: `./scripts/run_tests.sh`

The integration and end to end tests require a network connection.