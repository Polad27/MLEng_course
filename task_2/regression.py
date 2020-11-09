'''This script performs regression fitting'''
import json
import pickle
import yaml
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

def get_scaler(name):
    '''Returns suitable scaler'''
    if name == 'StandardScaler':
        return StandardScaler()
    if name == 'MinMaxScaler':
        return MinMaxScaler()
    if name == 'MaxAbsScaler':
        return MaxAbsScaler()
    raise 'Unsuitable name'

def metrics(y_true, y_pred):
    '''Calculate metrics'''
    return {'adj_r2': r2_score(y_true, y_pred),
            'MAE': mean_absolute_error(y_true, y_pred)}

params = yaml.safe_load(open('params.yaml'))
scaler = get_scaler(params['scaler'])

df = pd.read_csv('prepared_data.csv')

X_train, X_test, y_train, y_test = train_test_split(df.drop('C6H6(GT)', axis=1),
                                                    df['C6H6(GT)'])

lm = LinearRegression()
lm = lm.fit(scaler.fit_transform(X_train), y_train)

predicted = lm.predict(scaler.transform(X_test))

with open('scores.json', 'w') as f:
    json.dump(metrics(y_test, predicted), f)

with open('plots.json', 'w') as f:
    proc_dict = {'proc': [{
        'predicted': p,
        'real': r,
        } for p, r in zip(predicted, y_test)
    ]}
    json.dump(proc_dict, f)

with open('model.pkl', 'wb') as f:
    pickle.dump(lm, f)
