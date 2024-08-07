# -*- coding: utf-8 -*-

import os
from queries import get_channel_views_devices as get_views 
import sys
sys.path.insert(0, 'T:\\Public Relations\\ONLINE\\Passport\\STATS')

from helpers_process import normalize_shows
from helpers_queries import clean_passport_views as clean_views #needed for devices
from helpers_queries import set_aggregate #also needed for devices
from helpers_queries import prep_one_bar_horiz as plot


'''
settings
'''

#SEARCH DATES
date_start = '2016-04-01' #date Passport started

date_start = '2024-07-01'
date_end = '2024-08-01'

title = 'Top Channel Views'


'''
other setup
'''

#where output files go
root_graphics = 'output_graphics'
root_tables = 'output_tables'

#create needed folders if they don't exist
if not os.path.isdir(root_graphics): os.mkdir(root_graphics)
if not os.path.isdir(root_tables): os.mkdir(root_tables)
    
    
'''
process
'''

df = get_views(date_start, date_end)
df = normalize_shows(df, 'content_channel')
df = clean_views(df) #needed for devices
cols, plot_devices, aggreg_clust = set_aggregate(df, include_age=False) #also needed for devices

#get rid of unique ids/viewers
cols.remove('viewers')
aggreg_clust.pop('viewers') 
df = df.drop(['id'], axis=1)

#structure df for plot
sort_by = 'views'
df = df.groupby('show').agg(aggreg_clust)
df = df.sort_values(by=sort_by, ascending=False)
df = df[cols]

print('\n', df.head(20))
#print('\n', cols)
#print(plot_devices)
#print(aggreg_clust)

image = output_head = title.replace(' ', '_') + '.png'
plot(df, title, root_graphics, image, plot_devices=True)
