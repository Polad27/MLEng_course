import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import json
import yaml
import pickle

from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, SGDRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler
from sklearn.model_selection import cross_val_score, GridSearchCV, train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

def get_scaler(name):
    if name == 'StandardScaler':
        return StandardScaler()
    elif name == 'MinMaxScaler':
        return MinMaxScaler()
    elif name == 'MaxAbsScaler':
        return MaxAbsScaler()
    else:
        raise('Unsuitable name')

def metrics(real, predicted):
    # plt.scatter(x=predicted, y=real)
    # plt.show()
    return({'adj_r2': r2_score(real, predicted), 
            'MAE': mean_absolute_error(real, predicted)})

params = yaml.safe_load(open('params.yaml'))
scaler = get_scaler(params['scaler'])

df = pd.read_csv('prepared_data.csv')

X_train, X_test, y_train, y_test = train_test_split(df.drop('C6H6(GT)', axis=1), df['C6H6(GT)'])

lm = LinearRegression()
lm = lm.fit(scaler.fit_transform(X_train), y_train)

predicted = lm.predict(scaler.transform(X_test))
real = y_test



with open('scores.json', 'w') as f:
    json.dump(metrics(real, predicted), f)

with open('plots.json', 'w') as f:
    proc_dict = {'proc': [{
        'predicted': p,
        'real': r,
        } for p, r in zip(predicted, real)
    ]}
    json.dump(proc_dict, f)

with open('model.pkl', 'wb') as f:
    pickle.dump(lm, f)