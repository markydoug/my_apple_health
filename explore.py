import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

def plot_sleep_hours(df, year=0, month=0):
    '''
    Takes in sleep data df, year (>2010), month(numeric) and
    plots the total sleep hours for the whole dataset or 
    of the time frame you set.
    '''
    if (year > 2010) & (month > 0) & (month <=12):
        df = df[f'{year}-{month}']
        plt.bar(df.index, (df.total_time.dt.total_seconds()/60)/60)
        plt.title(f'Total number of Hours Slept by Day in {year}-{month}')
        plt.xlabel('Date')
        plt.ylabel('Hours')
        plt.axhline(y = ((df.total_time.dt.total_seconds()/60)/60).mean(), color = 'r', linestyle = '--', label=f'Average Sleep in Hours {((df.total_time.dt.total_seconds()/60)/60).mean():.2f}')
        plt.legend(loc='upper right', frameon=True)
        plt.show()
    elif (year > 2010):
        df = df[f'{year}']
        plt.bar(df.index, (df.total_time.dt.total_seconds()/60)/60)
        plt.title(f'Total number of Hours Slept by Day in {year}')
        plt.xlabel('Date')
        plt.ylabel('Hours')
        plt.axhline(y = ((df.total_time.dt.total_seconds()/60)/60).mean(), color = 'r', linestyle = '--', label=f'Average Sleep in Hours {((df.total_time.dt.total_seconds()/60)/60).mean():.2f}')
        plt.legend(loc='upper right', frameon=True)
        plt.show()
    else:
        plt.bar(df.index, (df.total_time.dt.total_seconds()/60)/60)
        plt.title(f'Total number of Hours Slept by Day')
        plt.xlabel('Date')
        plt.ylabel('Hours')
        plt.axhline(y = ((df.total_time.dt.total_seconds()/60)/60).mean(), color = 'r', linestyle = '--', label=f'Average Sleep in Hours {((df.total_time.dt.total_seconds()/60)/60).mean():.2f}')
        plt.legend(loc='upper right', frameon=True)
        plt.show()