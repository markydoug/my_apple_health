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

def compare_daily_stats(df):
    fig, ax = plt.subplots(4,1, figsize=(20,15))
    fig.tight_layout(pad=3.0)

    ax[0].plot(df.steps)
    ax[0].set_title('Total Steps')
    ax[0].set_ylabel('Steps')
    ax[0].axhline(df.steps.mean(), color = 'r', linestyle = '--', label=f'{round(df.steps.mean(),2)} steps')
    ax[0].legend(loc = 'upper right', frameon=True)

    ax[1].plot(df.weight)
    ax[1].set_title('Weight')
    ax[1].set_ylabel('kg')
    ax[1].axhline(df.weight.mean(), color = 'r', linestyle = '--', label=f'{round(df.weight.mean(),2)} kg')
    ax[1].legend(loc = 'upper right', frameon=True)

    ax[2].plot(df.resting_hr)
    ax[2].set_title('Resting HR')
    ax[2].set_ylabel('bpm')
    ax[2].axhline(df.resting_hr.mean(), color = 'r', linestyle = '--', label=f'{round(df.resting_hr.mean(),2)} bpm')
    ax[2].legend(loc = 'upper right', frameon=True)

    ax[3].plot(df.exercise_time)
    ax[3].set_title('Exercise Time')
    ax[3].set_ylabel('minutes')
    ax[3].axhline(df.exercise_time.mean(), color = 'r', linestyle = '--', label=f'{round(df.exercise_time.mean(),2)} min')
    ax[3].legend(loc = 'upper right', frameon=True)

    plt.show()

def show_daily_viz(df, year=0, month=0):
    if (year > 2010) & (month > 0) & (month <=12):
        df = df[f"{year}-{month}"]
        compare_daily_stats(df)

    elif (year > 2010):
        df = df[f"{year}"]
        compare_daily_stats(df)
    else:
        compare_daily_stats(df)