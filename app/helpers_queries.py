# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 13:49:44 2023

@author: pdriscoll
"""

import pandas as pd
import numpy as np
from graphs import one_bar_horiz 
from graphs import one_bar_horiz_3_stack 

#for use in clean_passport_views    
def map_devices(x):
    devices = {
        'Player': 'Browser',
        'Android': 'Mobile',
        'GA Roku': 'OTT',
        'Kids Roku': 'OTT',
        'IOS': 'Mobile',
        'GA Fire TV': 'OTT',
        'AppleTV App': 'OTT',
        'KIDS AppleTV App': 'OTT',
        'GA Android TV': 'OTT',
        'Video Portal': 'Browser',
        'Windows': 'Browser',
        'PartnerPlayer': 'Browser',
        'TVOS App': 'OTT',
        'Samsung TV': 'OTT',
        'Vizio TV': 'OTT'    
    }
    
    views = x['views']
    device = x['device']
    
    mobile = views if devices[device] == 'Mobile' else 0 
    browser = views if devices[device] == 'Browser' else 0       
    ott = views if devices[device] == 'OTT' else 0 

    return pd.Series([browser, mobile, ott])
    
#query cleanup
def clean_passport_views(df):
    if 'device' in df.columns: 
        df.columns = ['show', 'id', 'device', 'views', 'time']
        df[['browser', 'mobile', 'ott']] = df.apply(map_devices, axis=1)
        
        #for comparing different queries in testing    
        #df = df.drop(['browser', 'mobile', 'ott'], axis=1)
        
    else:
        df.columns = ['show', 'id', 'views', 'time']
    
    df['id'] = df['id'].fillna(0.0)	
    df = df.dropna()
    return df

def prep_one_bar_horiz(df, title, folder, image, plot_devices=False):
    df_plot = df.copy()
    df_plot = df_plot.head(10)
    df_plot = df_plot.sort_values(by='views')
    
    y_labels = df_plot.index.values.tolist()
    y_data = np.arange(len(y_labels))       
    
    if plot_devices:
        x_data = df_plot['views'].tolist() 
        x_data = df_plot[['browser', 'mobile', 'ott']]
        one_bar_horiz_3_stack(folder, image, title, y_labels, x_data, y_data)
        
    else:
        x_data = df_plot['views'].tolist() 
        one_bar_horiz(folder, image, title, y_labels, x_data, y_data) 
        
def set_aggregate(df, include_age=True):
    if include_age: cols = ['age', 'viewers', 'views']
    else: cols = ['viewers', 'views']
    
    plot_devices = False
    
    #set aggregation functions
    aggreg = {'views': 'sum', 'time': 'sum', 'viewers': 'nunique'}
              
    #add aggregate function to get average age for unique ids in each group
    #https://www.shanelynn.ie/summarising-aggregation-and-grouping-data-in-python-pandas/
    #https://stackoverflow.com/questions/14529838/apply-multiple-functions-to-multiple-groupby-columns          
    if include_age:
        aggreg['age'] = lambda g: g[df.ix[g.index]['viewers'].duplicated() == False].mean()

    if 'device' in df.columns: 
        devices = {'mobile': 'sum', 'browser': 'sum', 'ott': 'sum'}
        aggreg.update(devices)
        cols = cols + ['mobile', 'browser', 'ott']
        plot_devices = True
        
    return cols, plot_devices, aggreg