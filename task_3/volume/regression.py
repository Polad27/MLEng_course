'This script performs regression fitting'
import os
import pickle
import yaml
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from mlflow import log_metric, log_param, log_artifact, set_tracking_uri


def get_scaler(name):
    '''Returns suitable scaler'''
    if name == 'StandardScaler':
        return StandardScaler()
    if name == 'MinMaxScaler':
        return MinMaxScaler()
    if name == 'MaxAbsScaler':
        return MaxAbsScaler()
    raise Exception('Unsuitable name')


def metrics(y_true, y_pred):
    '''Calculate metrics'''
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    log_metric('Adjusted R-squared', r2)
    log_metric('Mean absolute error', mae)


def save_model(model, filename):
    '''Save model to pickle file'''
    if not os.path.exists('models'):
        os.makedirs('models')
    with open(f'models/{filename}.pkl', 'wb') as f:
        pickle.dump(model, f)


def save_importance(model, model_filename, features):
    '''''Save importance plot'''
    plt.barh(features, width=model.coef_)
    plt.savefig(f'models/{model_filename}_feat_imp_plot.png')
    log_artifact('models')


if __name__ == "__main__":

    df = pd.read_csv('prepared_data.csv')
    params = yaml.safe_load(open('params.yaml'))
    scaler_name = params['scaler']
    scaler = get_scaler(scaler_name)
    server = 'http://mlflow:5000'
    set_tracking_uri(server)
    log_param('Used Scaler', scaler)

    X_train, X_test, y_train, y_test = train_test_split(df.drop('C6H6(GT)', axis=1),
                                                        df['C6H6(GT)'], shuffle=False)

    lm = LinearRegression()
    lm = lm.fit(scaler.fit_transform(X_train), y_train)

    predicted = lm.predict(scaler.transform(X_test))
    model_filename = f'{scaler_name}_regression'

    metrics(y_test, predicted)
    save_model(lm, model_filename)
    save_importance(lm, model_filename, X_train.columns)