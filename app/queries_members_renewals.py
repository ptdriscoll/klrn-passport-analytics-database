# -*- coding: utf-8 -*-

'''
reference on byte order mark (BOM) for Windows in pd.to_csv
http://stackoverflow.com/questions/25788037/pandas-df-to-csvfile-csv-encode-utf-8-still-gives-trash-characters-for-min
'''

import pandas as pd
from queries import get_channel_episodes_views_members as get_pass
from graphs import pie_chart 


'''
settings
'''

#where email working folder is
root_folder = 'M:/FILES PATRICK/Alleg-Web/Emails/2017-07/'

#name of working file
file = 'Lists/email renewals 7-14-17.xlsx'

#where output files go
output_folder = root_folder + 'Passport/'

#MAKE SURE TO CHANGE SEARCH DATES
date_start = '2016-04-01'
date_end = '2017-07-31'

#these are output identifiers
output_tail = '2017_07'
output_head = 'Top_Channel_Views'

title = 'Top Channel Views'


'''
get members data
'''

df_mem = pd.read_excel(root_folder + file)
df_mem = df_mem.rename(columns = lambda x: x.strip())
#print '\n', df_mem.head(10)

df_mem = df_mem.rename(columns={'AcctID': 'id'})
df_mem['id'] = pd.to_numeric(df_mem['id'], errors='coerce')
#df_mem = df_mem.dropna()
df_mem['id'] = df_mem['id'].astype(int) 
output = 'Total Members:  ' + '{:,}'.format(len(df_mem.id.unique()))
#print '\n', df_mem.head()
#print '\n', df_mem.tail()


'''
get passport data
'''

df_pass = get_pass(date_start, date_end)

df_pass = df_pass.dropna()
df_pass['alleg_account_id'] = df_pass['alleg_account_id'].astype(int) 
df_pass = df_pass.sort_values('alleg_account_id', ascending=True)
df_pass.columns = ['channel', 'title', 'id', 'count']
output += '\n\nTotal Passport Members:  ' + '{:,}'.format(len(df_pass.id.unique()))
output += '\nTotal Views ' + '{:,}'.format(df_pass['count'].sum())
#print '\n',df_pass.head(10)

#check for any dups
#print '\nDUPS IN DF_PASS:',df_pass.set_index('id').index.get_duplicates()

df_pass = df_pass.set_index('id')


'''
merge member and passport data
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

df_mem_pass.to_csv(output_folder + 'renewals_pass.csv', index=False, encoding='utf-8')
df_mem_notpass.to_csv(output_folder + 'renewals_notpass.csv', index=False, encoding='utf-8')

#now prepare to merge members list with df_pass for viewing stats
#first clean dups
output += '\n\nDUPS IN df: ' + str(df.set_index('id').index.get_duplicates())
df = df.drop_duplicates()
df = df.set_index('id')
cols = df.columns.tolist()
#print '\nCHECK DEDUP:\n',df.loc[[290825, 451922, 1237064, 1499961]]

#next merge members list with df_pass 
df = df.join(df_pass, how='inner')
df = df.drop(cols, axis=1)
output += '\n\nPASSPORT MEMBERS: ' + str(df.shape[0]) + ' - or ' + '%.2f' % (100 * float(df.shape[0])/len(df_mem.id.unique())) + '%'
output += '\nTOTAL VIEWS: ' + '{:,}'.format(df['count'].sum())


'''
get top channel view 
'''

df_channels = df.copy()
df_channels = df_channels.groupby(['channel'])[['count']].sum()
df_channels = df_channels.sort_values('count', ascending=False)
output += '\n\n\nTOP CHANNELS:\n' + df_channels.head(10).to_string()

df_channels.to_csv(output_folder + output_head + '_channels_' + output_tail + '.csv', encoding='utf-8-sig')


'''
get top episode views
'''

df_episodes = df.copy()
df_episodes = df_episodes.groupby(['channel', 'title'])[['count']].sum()
df_episodes = df_episodes.sort_values('count', ascending=False)
df_episodes = df_episodes.reset_index(level='title')
output += '\n\n\nTOP EPISODES:\n' + df_episodes.set_index('title', drop=True).head(10).to_string()
output += '\n\n\nTOP EPISODES (SHOW CHANNELS)\n' + df_episodes.drop('title', axis=1).head(10).to_string()

df_episodes.to_csv(output_folder + output_head + '_episodes_' + output_tail + '.csv', encoding='utf-8-sig')

with open(output_folder + output_head + '_episodes_' + output_tail + '.txt', 'w') as of:  
    of.write(output.encode('utf-8'))
 
print '\n', output

#plot image of top channels   
inputf = df_channels.reset_index()      
outputf = output_folder + output_head + '.jpg'
print outputf
include_others = True

pie_chart(inputf, outputf, title, include_others) 