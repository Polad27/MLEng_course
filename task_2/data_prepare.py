import pandas as pd
from sklearn.impute import SimpleImputer

df = pd.read_csv('AirQualityUCI.csv', sep=';', na_values=-200, 
                 decimal=',', parse_dates=['Date', 'Time'])
df.dropna().to_csv('AirQualityUCI.csv')