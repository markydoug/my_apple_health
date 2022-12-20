import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

def plot_sleep_minutes(df, year, month)
    if (year > 2010) & (month > 0) & (month <=12):
        df = df[f'{year}-{month}']
        plt.bar(df.index, df.total_time.dt.total_seconds()/60)
    elif (year > 2010):
        df = df[f'{year}']
        plt.bar(df.index, df.total_time.dt.total_seconds()/60)
    else:
        plt.bar(df.index, df.total_time.dt.total_seconds()/60)