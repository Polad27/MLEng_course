
import os
import sys
import pandas as pd
import prophet as pt
import yfinance as yf


def create_time_dir(dt):
    '''Create dt directory'''
    print(os.listdir())
    dt = pd.to_datetime(dt, yearfirst=True)
    os.makedirs(os.path.join('/home/btc_forecaster/predictions/', dt.strftime('%Y%m%d')), 
                exist_ok=True, mode=0o777)
    return os.path.join('/home/btc_forecaster/predictions/', dt.strftime('%Y%m%d')), dt.strftime('%Y%m%d_%H%M.csv')


def forecast(ticker, train_period, prediction_horizon, dt):
    '''Make forecast for selected horizon'''
    end = pd.to_datetime(dt)
    start = end - pd.Timedelta(days=train_period)
    print('Retrieving data')
    df = yf.Ticker(ticker)\
           .history(start=start.to_pydatetime(),
                    end=end.to_pydatetime(), 
                    interval='1m')
    df.index = df.index.tz_localize(None)  
    df.index = df.index.floor('1min')
    df = df.reset_index()\
           .rename(columns={'Datetime': 'ds', 'Close': 'y'})\
           .loc[:, ['ds', 'y']]
    print('Model fitting')
    model = pt.Prophet()
    model.fit(df)
    print('Forecasting')
    forecast_df = model.predict(model.make_future_dataframe(periods=prediction_horizon, 
                                                            freq='1min', 
                                                            include_history=False))[['ds', 'yhat']]
    forecast_df.ds = forecast_df.ds.dt.tz_localize('UTC')
    return forecast_df

if __name__ == '__main__':
    dt = str(sys.argv[1])
    path, filename = create_time_dir(dt)
    forecast('BTC-USD', 7, 5, dt).to_csv(os.path.join(path, filename), index=False)