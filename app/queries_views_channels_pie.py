# -*- coding: utf-8 -*-

import os
from helpers import normalize_shows
from queries import get_channel_views
from graphs import pie_chart 

'''
settings
'''

#SEARCH DATES
date_start = '2016-04-01'
date_start = '2020-08-01'
date_end = '2020-09-01'

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

#get passport data
df = get_channel_views(date_start, date_end)
df = normalize_shows(df, 'content_channel', regroup=True)
output_head = title.replace(' ', '_')
df.to_csv(root_tables + '/' + output_head + '.csv', index=False, encoding='utf-8-sig')
print df.head(20)
print '\nTOTAL VIEWS', df['total_count'].sum()

#plot results    
inputf = df      
outputf = os.path.join(root_graphics, output_head + '.png')
include_others = True





pie_chart(inputf, outputf, title, include_others)




