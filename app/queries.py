# -*- coding: utf-8 -*-

import os
import pandas as pd
import sqlite3


'''
start and stop searches in below functions use this format 2016-04-01 
'''

def get_data_in_dataframe(query):  
    loc_database = os.path.join(os.path.dirname(__file__), 'database', 'db.sqlite')
    conn = sqlite3.connect(loc_database)
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df

def get_channel_views(date_start, date_end):
    query = '''
        SELECT 
          Videos.content_channel, 
          COUNT(Views.id) AS total_count
        FROM Videos	
        INNER JOIN Views ON Videos.media_id = Views.videos_media_id 
        WHERE Views.date_time >= datetime('{} 00:00:00', 'localtime')
        AND Views.date_time <= datetime('{} 00:00:00', 'localtime')
        GROUP BY Videos.content_channel
        ORDER BY total_count DESC;
    '''.format(date_start, date_end)

    return get_data_in_dataframe(query)

#this includes devices
def get_channel_views_devices(date_start, date_end):
    query = '''
        SELECT 
          Videos.content_channel,
          Members.alleg_account_id,
          Views.device,
          COUNT(Views.id) AS total_count,
          SUM(Views.time_watched) AS time_watched
        FROM Views	
        INNER JOIN Videos ON Views.videos_media_id = Videos.media_id  
        INNER JOIN Members ON Views.members_uid = Members.uid
        WHERE Views.date_time >= datetime('{}', 'localtime')
        AND Views.date_time <= datetime('{}', 'localtime')
        GROUP BY Videos.content_channel, Members.alleg_account_id, Views.device
        ORDER BY total_count DESC;
    '''.format(date_start, date_end) 

    return get_data_in_dataframe(query)

def get_views_members(date_start, date_end):
    query = '''
        SELECT 
          Members.alleg_account_id,
          COUNT(Views.id) AS total_count
        FROM Views	
        INNER JOIN Videos ON Views.videos_media_id = Videos.media_id  
        INNER JOIN Members ON Views.members_uid = Members.uid
        WHERE Views.date_time >= datetime('{} 00:00:00', 'localtime')
        AND Views.date_time <= datetime('{} 00:00:00', 'localtime')
        GROUP BY Members.alleg_account_id
        ORDER BY total_count DESC;
    '''.format(date_start, date_end)

    return get_data_in_dataframe(query)
    
def get_channel_views_members(date_start, date_end, ids):
    query = '''
        SELECT 
          Videos.content_channel,
          Members.alleg_account_id,
          COUNT(Views.id) AS total_count
        FROM Views	
        INNER JOIN Videos ON Views.videos_media_id = Videos.media_id  
        INNER JOIN Members ON Views.members_uid = Members.uid
        WHERE Views.date_time >= datetime('{} 00:00:00', 'localtime')
        AND Views.date_time <= datetime('{} 00:00:00', 'localtime')
        AND Members.alleg_account_id IN ({})
        GROUP BY Videos.content_channel, Members.alleg_account_id
        ORDER BY total_count DESC;
    '''.format(date_start, date_end, ids)

    return get_data_in_dataframe(query)    

def get_channel_views_genres_members(date_start, date_end, ids):
    """
    Unlike most other queries, this is sorted by date so that a code aggregation can get latest genre values.
    """
    query = '''
        SELECT 
          Videos.content_channel,
          Members.alleg_account_id,
          COUNT(Views.id) AS total_count,
          Videos.genre
        FROM Views	
        INNER JOIN Videos ON Views.videos_media_id = Videos.media_id  
        INNER JOIN Members ON Views.members_uid = Members.uid
        WHERE Views.date_time >= datetime('{} 00:00:00', 'localtime')
        AND Views.date_time <= datetime('{} 00:00:00', 'localtime')
        AND Members.alleg_account_id IN ({})
        GROUP BY Videos.content_channel, Members.alleg_account_id
        ORDER BY Views.date_time;
    '''.format(date_start, date_end, ids)

    return get_data_in_dataframe(query)  
 
def get_channel_episodes_views_members(date_start, date_end, ids):
    query = '''
        SELECT 
          Videos.content_channel,
          Videos.title,
          Members.alleg_account_id,
          COUNT(Views.id) AS total_count
        FROM Views	
        INNER JOIN Videos ON Views.videos_media_id = Videos.media_id  
        INNER JOIN Members ON Views.members_uid = Members.uid
        WHERE Views.date_time >= datetime('{} 00:00:00', 'localtime')
        AND Views.date_time <= datetime('{} 00:00:00', 'localtime')
        AND Members.alleg_account_id IN ({})
        GROUP BY Videos.content_channel, Videos.title, Members.alleg_account_id
        ORDER BY total_count DESC;
    '''.format(date_start, date_end, ids)

    return get_data_in_dataframe(query)
