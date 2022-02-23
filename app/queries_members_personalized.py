# -*- coding: utf-8 -*-

import os
import pandas as pd
from queries import get_channel_views_members as get_views


"""
manual settings
"""

#working directory (inside root directory)
root_dir = 'T:\\Public Relations\\FILES PATRICK\\Alleg-Web\\Emails'
working_dir = 'Major-Donors-2022-01'
output_dir = 'Passport'

#name of input file (in ROOT directory)
input_file = 'MD Pull 28 Dec' + '.csv'
input_file = 'Passport\\Top_Views_Renewals_pass' + '.csv'

#search dates
date_start = '2021-01-01'
date_end = '2022-01-01'

#number of top shows to query for each member
num_top_shows = 3

"""
auto settings
"""

input_f = os.path.join(root_dir, working_dir, input_file) 
output_f = os.path.join(root_dir, working_dir, output_dir, 'Top_Views_personalized.csv')

"""
get top shows and views for each member
"""

df_mem = pd.read_csv(input_f).head()
df_mem = pd.read_csv(input_f)

df_mem = df_mem.rename(columns = {'id': 'AcctID'})

#create list of cols for top shows and views: Top_Show_1, Show_1_Views, ...
f1 = lambda x: 'Top_Show_' + str(x+1)
f2 = lambda x: 'Views_' + str(x+1)
cols = ['AcctID'] + [f(x) for x in range(num_top_shows) for f in (f1,f2)]

'''
to refactor next section for renewals eblasts:
    - add list of shows to filter out of returned results because they will instead be in all emails
    - add list of shows to add (in f1 function) when returned results is less than num_top_shows
'''

#loop members and run sql query to get top shows and views for each
#https://www.kite.com/python/answers/how-to-build-a-pandas-dataframe-with-a-for-loop-in-python
mem_ids = [x for x in df_mem['AcctID']]

rows = []
print('')
for id in mem_ids:
    df_views = get_views(date_start, date_end, id)
    shows = df_views['content_channel'].head(num_top_shows) 
    views = df_views['total_count'].head(num_top_shows).astype(str) 
    
    f1 = lambda x: shows[x] if x < len(shows) else ''
    f2 = lambda x: views[x] if x < len(views) else ''
    row = [id] + [f(x) for x in range(num_top_shows) for f in (f1,f2)]
    rows.append(row)
    print(str(len(rows)) + ' - Added AcctID ' + str(id))
    
print('\nFINISHED')    

#output new spreadsheet    
df_shows = pd.DataFrame(rows, columns=cols)
df_merged = df_mem.merge(df_shows, on='AcctID')

print('')
print(df_merged.head())

df_merged.to_csv(output_f, index=False, encoding='utf-8')
    