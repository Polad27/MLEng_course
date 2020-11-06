import pandas as pd

df = pd.read_csv('AirQualityUCI.csv', sep=';', na_values=-200, decimal=',')\
	   .drop(columns=['Date', 'Time', 'Unnamed: 15', 'Unnamed: 16', 'NMHC(GT)'])
df.dropna().to_csv('prepared_data.csv', index=False)