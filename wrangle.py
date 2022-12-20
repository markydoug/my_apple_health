import xmltodict
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import os

def xml_to_df(section, xml='导出.xml'):
    file = open(xml,'r')
    contents = file.read()

    input_data = xmltodict.parse(contents)
    df = pd.DataFrame(input_data['HealthData'][section])

    return df

def get_health_data(section):
    ''' 
    Checks to see if there is a local copy of the data, 
    if not go get data from github
    '''
    filename = f'{section}.csv'
    #if we don't have cached data or we want to get new data go get it from server
    if (os.path.isfile(filename) == False):
        df = xml_to_df(section)
        #save as csv
        df.to_csv(filename,index=False)

    #else used cached data
    else:
        df = pd.read_csv(filename)

    return df

def clean_records_list(df):
    df = df.rename(columns = {'@type': 'activity_type',
                         '@sourceName': 'source',
                         '@sourceVersion': 'source_ver',
                         '@unit': 'unit_of_measure',
                         '@creationDate': 'creation_time',
                         '@startDate': 'activity_start_time',
                         '@endDate': 'activity_end_time',
                         '@value': 'value',
                         'MetadataEntry': 'metadata',
                         '@device': 'device'})
    #drop metadata columns
    df = df.drop(columns = ['HeartRateVariabilityMetadataList','metadata'])

    # shorter observation names
    df['activity_type'] = df['activity_type'].str.replace('HKQuantityTypeIdentifier', '')
    df['activity_type'] = df['activity_type'].str.replace('HKCategoryTypeIdentifier', '')
    df['activity_type'] = df['activity_type'].str.replace('HKDataType', '')

    #drop nulls in value column
    df.dropna(subset='value', inplace=True)

    return df

def change_time_zone(df):
    #convert index timezone
    df = df.tz_convert('Asia/Chongqing')
    #convert activity_start_time timezone
    df['activity_start_time'] = df['activity_start_time'].dt.tz_convert('Asia/Chongqing')
    #convert activity_end_time timezone
    df['activity_end_time'] = df['activity_end_time'].dt.tz_convert('Asia/Chongqing')
    df['in_china'] = 1
    return df

def add_date(df):
    df['date'] = df['activity_start_time'].dt.strftime('%Y/%m/%d')
    return df

def add_times(df):
    df['start_time'] = df['activity_start_time'].dt.strftime('%H:%M')
    df['end_time'] = df['activity_end_time'].dt.strftime('%H:%M')
    df['total_time'] = df['activity_end_time'] - df['activity_start_time']
    return df

def records_list_time_zone_fun(df):
    df['creation_time'] = pd.to_datetime(df['creation_time'])
    df['activity_start_time'] = pd.to_datetime(df['activity_start_time'])
    df['activity_end_time'] = pd.to_datetime(df['activity_end_time'])
    df = df.set_index('creation_time').sort_index()

    #separate time periods
    china1 = df[:'2016-11-21 11']
    us1 = df['2016-11-21 20':'2017-01-12 17']
    china2 = df['2017-01-12 17':'2017-05-01 08']
    us2 = df['2017-05-01 08':'2017-06-06 01']
    china3 = df['2017-06-06 01':'2018-07-11 12']
    us3 = df['2018-07-11 12':'2018-08-24 10']
    china4 = df['2018-08-24 10':'2019-08-02 11']
    us4 = df['2019-08-02 11':'2019-08-16 02']
    china5 = df['2019-08-16 02':'2020-01-29 10']
    us5 = df['2020-01-29 10':'2020-02-13 16']
    china6 = df['2020-02-13 17':'2022-03-02 15']
    us6 = df['2022-03-02 16':]

    #convert time zones of those time periods when I was in China
    china1 = change_time_zone(china1)
    china2 = change_time_zone(china2)
    china3 = change_time_zone(china3)
    china4 = change_time_zone(china4)
    china5 = change_time_zone(china5)
    china6 = change_time_zone(china6)

    #
    china1 = add_date(china1)
    china2 = add_date(china2)
    china3 = add_date(china3)
    china4 = add_date(china4)
    china5 = add_date(china5)
    china6 = add_date(china6)

    china1 = add_times(china1)
    china2 = add_times(china2)
    china3 = add_times(china3)
    china4 = add_times(china4)
    china5 = add_times(china5)
    china6 = add_times(china6)

    us1 = add_date(us1)
    us2 = add_date(us2)
    us3 = add_date(us3)
    us4 = add_date(us4)
    us5 = add_date(us5)
    us6 = add_date(us6)

    us1 = add_times(us1)
    us2 = add_times(us2)
    us3 = add_times(us3)
    us4 = add_times(us4)
    us5 = add_times(us5)
    us6 = add_times(us6)

    df = pd.concat([china1,us1,china2,us2,china3,us3,china4,us4,china5,us5,china6,us6])

    df['in_china'].fillna(0, inplace=True)
    df['in_china'] = df['in_china'].astype('uint8')
    df['date'] = pd.to_datetime(df['date'])
    df = df.drop(columns = ['activity_start_time','activity_end_time'])
    df = df.set_index('date').sort_index()

    return df

def get_steps(df):
    '''
    Take in records df and returns the steps not associated with XiaoMi
    YunDong and concats the steps from my phone and the steps from my
    Apple Watch
    '''
    df = df[df['activity_type'] == 'StepCount']
    df.value = df.value.astype(int)
    df =df[df.source != '小米运动']
    phone_steps = df[df['source'] == 'Marky Doug']
    apple_watch_steps = df[df['source'] != 'Marky Doug']
    df = phone_steps.loc[:'2021-10-28'].append(apple_watch_steps)

    return df

def get_active_energy(df):
    df = df[df['activity_type'] == 'ActiveEnergyBurned']
    df['value'] = df['value'].astype(int)

    return df

def get_sleep_data(df):
    df = df[df['activity_type'] == 'SleepAnalysis']
    df['value'] = df['value'].str.replace('HKCategoryValueSleepAnalysis', '')
    
    return df

