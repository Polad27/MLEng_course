import os
import sys
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

from sklearn.metrics import mean_absolute_percentage_error as mape


def move_to_dt_dir(dt):
    '''Move to current predictions dir'''
    dt = pd.to_datetime(dt, yearfirst=True).strftime('%Y%m%d')
    os.chdir(os.path.join('/home/btc_forecaster/predictions/', dt))


def evaluate(ticker):
    '''Evaluate model performance'''
    print('Retrieving data')
    predictions = pd.concat([pd.read_csv(f, parse_dates=['ds']) for f in os.listdir() if f.endswith('.csv')])
    df = yf.Ticker(ticker)\
           .history(start=predictions.ds.min().to_pydatetime(),
                    end=predictions.ds.max().to_pydatetime(), 
                    interval='1m')
    df.index = df.index.floor('1min')
    df.index = df.index.tz_convert('UTC')
    df = df.loc[predictions.ds.min():predictions.ds.max()]
    df = df.reset_index()
    df = df.merge(predictions, left_on='Datetime', right_on='ds', how='inner')\
           .rename(columns={'Close': 'Actuals', 'yhat': 'Predicted'})\
           .set_index('Datetime')
    df = df[['Actuals', 'Predicted']]
    print('Metric calculation')
    mape_value = mape(df.Actuals, df.Predicted) * 100
    print('Plotting')
    df.plot(title=f'Actuals vs. Predicted MAPE={round(mape_value, 2)}%')
    plt.savefig('forecast_plot.png', dpi=400)


if __name__ == '__main__':
    dt = str(sys.argv[1])
    move_to_dt_dir(dt)
    evaluate('BTC-USD')