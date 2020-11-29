'''This script prepares data'''
import pandas as pd
import yaml
from mlflow import log_param


if __name__ == '__main__':
	params = yaml.safe_load(open('params.yaml'))
	na_values = params['data_preparation']['na_values']
	drop_columns = params['data_preparation']['drop_columns']

	df = pd.read_csv('AirQualityUCI.csv', sep=';', na_values=na_values, decimal=',')\
		   .drop(columns=drop_columns)
	df.dropna().to_csv('prepared_data.csv', index=False)
	log_param('Data prepared', True)
