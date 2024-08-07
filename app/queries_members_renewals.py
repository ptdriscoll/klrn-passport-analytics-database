# -*- coding: utf-8 -*-

import os
import pandas as pd
from queries import get_views_members as get_pass
from queries import get_channel_episodes_views_members as get_views
from graphs import pie_chart 


'''
manual settings
'''

#stats to run = reg' or 'maj'
to_run = 'reg'
#to_run = 'maj'

#name of working file
file_regular = 'Lists\\' + 'membership email renewals 7-22-24' + '.xlsx'
file_major = 'Lists\\' + '' + '.xlsx'

#these are output identifiers
output_dir = '2024-07'
#output_dir = 'Major-Donors-2022-01'

#MAKE SURE TO CHANGE SEARCH DATES
date_start = '2023-07-01'
date_end = '2024-07-01'


'''
auto settings
'''

#where email working folder is
root_folder = 'T:\\Public Relations\\FILES PATRICK\\Alleg-Web\\Emails\\' + output_dir + '/'

if to_run == 'reg': 
    f = file_regular
    output_head = 'Top_Views_Renewals'
    title = 'Top Views - Renewals'

if to_run == 'maj':
    f = file_major
    output_head = 'Top_Views_Major'
    title = 'Top Views - Major Renewals'

#where output files go
output_folder = root_folder + 'Passport/'

output_tail = output_dir.replace('-', '_')


'''
create output folder if needed
'''

if not os.path.isdir(output_folder): 
    os.mkdir(output_folder)


'''
get members data
'''

df_mem = pd.read_excel(root_folder + f)
df_mem = df_mem.rename(columns = lambda x: x.strip())
#print('\n', df_mem.head(10))

df_mem = df_mem.rename(columns={'AcctID': 'id'})
df_mem['id'] = pd.to_numeric(df_mem['id'], errors='coerce')
#df_mem = df_mem.dropna()
df_mem['id'] = df_mem['id'].astype(int) 
output = 'Total Members:  ' + '{:,}'.format(len(df_mem.id.unique()))
#print('\n', df_mem.head())
#print('\n', df_mem.tail())


'''
get total passport viewers
'''

df_pass = get_pass(date_start, date_end)

df_pass = df_pass.dropna()
df_pass['alleg_account_id'] = df_pass['alleg_account_id'].astype(int) 
df_pass = df_pass.sort_values('alleg_account_id', ascending=True)
df_pass.columns = ['id', 'count']
output += '\n\nTotal Passport Viewers:  ' + '{:,}'.format(len(df_pass.id.unique()))
output += '\nTotal Views ' + '{:,}'.format(df_pass['count'].sum())
#print('\n',df_pass.head(10))

#check for any dups
#print('\nDUPS IN DF_PASS:',df_pass.set_index('id').index.get_duplicates())

df_pass = df_pass.set_index('id')


'''
split members by passport viewers
'''

df = df_mem.copy()

#first split the members list for seperate tracking later
pass_ids = df_pass.index.values.tolist()
df_mem_pass = df[df['id'].isin(pass_ids)] 
df_mem_notpass = df[~df['id'].isin(pass_ids)] 

output += '\n\nCHECK SPLIT MEMBER LISTS:'
output += '\n' + str(df.shape)
output += '\n' + str(df_mem_pass.shape)
output += '\n' + str(df_mem_notpass.shape)
pass_percent = (float(df_mem_pass.shape[0]) / df.shape[0]) * 100
output += '\nPassport viewers: {0:.0f}%'.format(pass_percent)

df_mem_pass.to_csv(output_folder + output_head + '_pass.csv', index=False, encoding='utf-8-sig')
df_mem_notpass.to_csv(output_folder + output_head + '_notpass.csv', index=False, encoding='utf-8-sig')


'''
get segmented channel and episode viewers 
'''

df = df_mem_pass.copy()

#clean dups
output += '\n\nDUPS IN df: ' + str(df['id'][df['id'].duplicated()])
df = df.drop_duplicates(subset=['id'])
df = df.set_index('id')
cols = df.columns.tolist()


#run search based on segmented member ids
mem_pass_ids = df.index.values.tolist()
mem_pass_ids = ','.join(str(x) for x in mem_pass_ids)
df_views = get_views(date_start, date_end, mem_pass_ids)
df_views.columns = ['channel', 'title', 'id', 'count']


'''
get top channel views 
'''

df_channels = df_views.copy()
df_channels = df_channels.groupby(['channel'])[['count']].sum()
df_channels = df_channels.sort_values('count', ascending=False)
output += '\n\n\nTOP CHANNELS:\n' + df_channels.head(10).to_string()

df_channels.to_csv(output_folder + output_head + '_channels_' + output_tail + '.csv', encoding='utf-8-sig')


'''
get top episode views
'''

df_episodes = df_views.copy()
df_episodes = df_episodes.groupby(['channel', 'title'])[['count']].sum()
df_episodes = df_episodes.sort_values('count', ascending=False)
df_episodes = df_episodes.reset_index(level='title')
output += '\n\n\nTOP EPISODES\n' + df_episodes.head(10).to_string()
output += '\n'

df_episodes.to_csv(output_folder + output_head + '_episodes_' + output_tail + '.csv', encoding='utf-8-sig')

with open(output_folder + output_head + output_tail + '.txt', 'w') as of:  
    of.write(output)
 
print('\n', output)

#plot image of top channels   
inputf = df_channels.reset_index()      
outputf = output_folder + output_head + '.png'
print(outputf)
include_others = True

pie_chart(inputf, outputf, title, include_others) 
