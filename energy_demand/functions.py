import pandas as pd
import datetime as dt
import requests
import numpy as np
from io import StringIO


def get_data():
    """ load energy and temperature data from data\ folder
    and returns it in a dictionary with two dataframes """
    energy_data = pd.read_csv(r'data\energy.dat')
    energy_data.set_index('Date', inplace=True)
    energy_data.index = pd.to_datetime(energy_data.index)
    temp_data = pd.read_csv(r'data\uk_temps.csv')
    temp_data.set_index('Date', inplace=True)
    temp_data.index = pd.to_datetime(temp_data.index)
    return {'energy_data': energy_data, 'temp_data': temp_data}


def download_uk_temp_data():
    """ downloads uk mean temperature from 1700 to today and saves it in a csv"""
    temp_data = requests.get('https://www.metoffice.gov.uk/hadobs/hadcet/data/meantemp_daily_totals.txt')
    csvStringIO = StringIO(temp_data.text)
    temp_data = pd.read_csv(csvStringIO)  # delim_whitespace=True)
    temp_data.columns = ['datevalue']
    temp_data['Date'] = pd.to_datetime(temp_data['datevalue'].apply(lambda x: x.split(' ')[0]))
    temp_data['Value'] = temp_data['datevalue'].apply(lambda x: float(x.split(' ')[-1]))
    temp_data = temp_data.set_index('Date')[['Value']]
    temp_data = temp_data['1980-01-01':]
    temp_data.to_csv(r'data\uk_temps.csv')


def create_variables_df(raw_data, c=True, trend=True, wds=True, months=True, holidays=True,
                           hdds=False, temps=False, temp_df=None):
    """  """

    if c:
        raw_data['C'] = 1
    if trend:
        raw_data['trend'] = raw_data.index.map(lambda x: (x - dt.datetime(2015, 4, 1)).days / 365)

    if hdds or temps:
        if temp_df is None:
            raise Exception("if temps or hdds is True, you need to pass temp_df")
        raw_data['Temp'] = raw_data.join(temp_df)['Value']

    if hdds:
        raw_data['HDD18'] = raw_data['Temp'].apply(lambda x: max(18 - x, 0))
        raw_data.drop('Temp', axis=1, inplace=True)

    if wds:
        for wd in range(7):
            raw_data[f'wd_{wd}'] = raw_data.index.map(lambda x: 1 if x.weekday() == wd else 0)
    if months:
        for month in range(12):
            raw_data[f'month_{month}'] = raw_data.index.map(lambda x: 1 if x.month == month+1 else 0)
    if holidays:
        pass
    return raw_data


def fourier_analysis(ts, num_freq=10):
    """  Takes a series and return relevant frequencies
    Args:
        ts: numpy array, the series to analyse
        num_freq: int, number of frequencies to return
    Returns:
        pandas df with cols ['period', 'nspectrum'] and length = num_freq
    """
    x = list(range(len(ts.index)))
    # apply fast fourier transform and take absolute values
    f=abs(np.fft.fft(ts))

    # get the list of frequencies
    num=np.size(x)
    freq = [i / num for i in list(range(num))]

    # get the list of spectrums
    spectrum=f.real*f.real+f.imag*f.imag
    nspectrum=spectrum/spectrum[0]

    # improve the plot by adding periods in number of weeks rather than  frequency
    results = pd.DataFrame({'freq': freq, 'nspectrum': nspectrum})
    results['period'] = 1/results['freq']

    # improve the plot by convertint the data into grouped per week to avoid peaks
    results['period_round'] = results['period'].round()
    grouped_df = results.groupby('period_round').sum()[['nspectrum']].drop(np.inf,axis=0)
    threshold = grouped_df.sort_values('nspectrum').iloc[num_freq*-1]['nspectrum']
    final_df = grouped_df[grouped_df['nspectrum'] > threshold].reset_index()
    final_df['period_round'] = final_df['period_round'].apply(lambda x: str(int(x)) + '_days')
    return final_df



if __name__ == '__main__':
    download_uk_temp_data()
