# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
from queries import get_views_members as get_pass
from queries import get_channel_views_members as get_views
from graphs import pie_chart 


'''
settings
'''

#make sure excel input file is named after end date 
#for example, use this naming scheme, members_2017-05-31
#also make sure excel input file is in members folder
date_start = '2016-04-01'
date_end = '2017-05-31'


'''
other setup
'''

#where output files go
root_graphics = 'output_graphics'
root_tables = 'output_tables'

#create needed folders if they don't exist
if not os.path.isdir(root_graphics): os.mkdir(root_graphics)
if not os.path.isdir(root_tables): os.mkdir(root_tables)
    
#this just makes sure names are more python-lie
date_naming = date_end.replace('-', '_')    
    

'''
get members data
'''

df_mem = pd.read_excel('members/members_{}.xlsx'.format(date_naming))
df_mem = df_mem.rename(columns = lambda x: x.strip())
#print '\n', df_mem.head(10)

new_cols = ['id', 'sustainer', 'first_donation', 'major_donor']
df_mem = pd.DataFrame(df_mem['Each -'].str.split(' - ', 4).tolist(), columns=new_cols)
df_mem['id'] = pd.to_numeric(df_mem['id'], errors='coerce')
df_mem = df_mem.dropna()
df_mem['id'] = df_mem['id'].astype(int) 
print '\nTotal Members: ', '{:,}'.format(len(df_mem.id.unique()))
#print '\n', df_mem.head()
#print '\n', df_mem.tail()


'''
get total passport viewers
'''

df_pass = get_pass(date_start, date_end)

df_pass = df_pass.dropna()
df_pass['alleg_account_id'] = df_pass['alleg_account_id'].astype(int) 
df_pass = df_pass.sort_values('alleg_account_id', ascending=True)
df_pass.columns = ['id', 'count']
print '\nTotal Passport Members: ', '{:,}'.format(len(df_pass.id.unique()))
print 'Total Views',df_pass['count'].sum()
#print '\n',df_pass.head(10)

#check for any dups
#print '\nDUPS IN DF_PASS:',df_pass.set_index('id').index.get_duplicates()

df_pass = df_pass.set_index('id')


'''
sustainer segment
'''

#create from df_mem
df_sust = df_mem[['id', 'sustainer']].copy()
df_sust['sustainer'] = df_sust['sustainer'].str.strip() 
df_sust = df_sust[df_sust['sustainer'] == 'ACT']

#clean dups
#print '\nDUPS IN DF_SUST:',df_sust.set_index('id').index.get_duplicates()
df_sust = df_sust.drop_duplicates()
df_sust = df_sust.set_index('id')
#print '\nCHECK DEDUP:\n',df_sust.loc[[290825, 451922, 1237064, 1499961]]

#run search based on segmented member ids
df_sust_ids = df_sust.index.values.tolist()
df_sust_ids = ','.join(str(x) for x in df_sust_ids)
df_sust = get_views(date_start, date_end, df_sust_ids)
df_sust.columns = ['channel', 'id', 'count']
print '\n\nSUSTAINERS:', df_sust.shape
print 'TOTAL VIEWS:', '{:,}'.format(df_sust['count'].sum())

#sum and print 
df_sust = df_sust.groupby(['channel'])[['count']].sum()
df_sust = df_sust.sort_values('count', ascending=False)
print df_sust.head(10)

df_sust.to_csv(root_tables + '/df_sust_{}.csv'.format(date_naming), encoding='utf-8')

#plot results    
inputf = df_sust.reset_index()      
outputf = os.path.join(root_graphics, 'Sustainer_Channels.jpg')
title = 'Sustainer Top Channels'
include_others = True

print ''
pie_chart(inputf, outputf, title, include_others) 
print ''


'''
first-year segment
'''

#create from df_mem
df_first = df_mem[['id', 'first_donation']].copy()
df_first['first_donation'] = df_first['first_donation'].str.strip() 
df_first = df_first[df_first['first_donation'] == 'NEW']

#check for dups
#print '\nDUPS IN DF_FIRST:',df_first.set_index('id').index.get_duplicates()
df_first = df_first.set_index('id')

#run search based on segmented member ids
df_first_ids = df_first.index.values.tolist()
df_first_ids = ','.join(str(x) for x in df_first_ids)
df_first = get_views(date_start, date_end, df_first_ids)
df_first.columns = ['channel', 'id', 'count']
print '\n\nSUSTAINERS:', df_first.shape
print 'TOTAL VIEWS:', '{:,}'.format(df_first['count'].sum())

#sum and print 
df_first = df_first.groupby(['channel'])[['count']].sum()
df_first = df_first.sort_values('count', ascending=False)
print df_first.head(10)

df_first.to_csv(root_tables + '/df_first_{}.csv'.format(date_naming), encoding='utf-8')

#plot results    
inputf = df_first.reset_index()      
outputf = os.path.join(root_graphics, 'First_Time_Channels.jpg')
title = 'First-Time Donor Top Channels'
include_others = True

print ''
pie_chart(inputf, outputf, title, include_others) 
print ''


'''
major donors segment
'''

#create from df_mem
df_major = df_mem[['id', 'major_donor']].copy()
df_major['major_donor'] = df_major['major_donor'].str.strip() 
df_major['major_donor'] = df_major['major_donor'].replace('', np.nan)
df_major = df_major.dropna() 
#df_major = df_major[(df_major['major_donor'] == 'A')]
df_major = df_major.sort_values('major_donor', ascending=True)
print '\n',df_major.head(20)

#clean dups
#print '\nDUPS IN df_major:',df_major.set_index('id').index.get_duplicates()
df_major = df_major.drop_duplicates()
#print '\nRECHECK DUPS IN df_major:',df_major.set_index('id').index.get_duplicates()
df_major = df_major.set_index('id')
#print '\nCHECK DEDUP:\n',df_major.loc[[116970, 134346, 150375, 154096]]

#run search based on segmented member ids
df_major_ids = df_major.index.values.tolist()
df_major_ids = ','.join(str(x) for x in df_major_ids)
df_major = get_views(date_start, date_end, df_major_ids)
df_major.columns = ['channel', 'id', 'count']
print '\n\nSUSTAINERS:', df_major.shape
print 'TOTAL VIEWS:', '{:,}'.format(df_major['count'].sum())

#sum and print 
df_major = df_major.groupby(['channel'])[['count']].sum()
df_major = df_major.sort_values('count', ascending=False)
print df_major.head(10)

df_major.to_csv(root_tables + '/df_major_{}.csv'.format(date_naming), encoding='utf-8')

#plot results    
inputf = df_major.reset_index()      
outputf = os.path.join(root_graphics, 'Major_Donor_Channels.jpg')
title = 'Major-Gift Donor Top Channels'
include_others = True

print ''
pie_chart(inputf, outputf, title, include_others) 