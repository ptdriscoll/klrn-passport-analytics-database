# -*- coding: utf-8 -*-

import sqlite3
import shutil
import zipfile
import os
import glob
import pandas as pd
import numpy as np
import helpers_process as helpers 
from db_backup import database_backup, delete_old_backups 


'''
settings
'''

#prepare list of zip files for processing
#these zip files must be in a folder called downloads

#multiple zip files can be listed - which is important to seed start
toParse = [  
    '2024_08_01_10_16_00.zip',
]


'''
setup process files, and database  
'''

#create needed folders if they don't exist
if not os.path.isdir('database'): os.mkdir('database')
if not os.path.isdir('committed'): os.mkdir('committed')
        
#clean out or create processing folder
if os.path.isdir('processing'):
    shutil.rmtree('processing', ignore_errors=False, onerror=None)
os.mkdir('processing')

#unzip directories to be processed
print('\nTO PROCESS:')
for file in toParse:
    print('\tdownloads/' + file)
    directoryName = file.rstrip('.zip')
    newDirectory = os.mkdir('processing/' + directoryName)    
    with zipfile.ZipFile('downloads/' + file) as toExtract:
        toExtract.extractall('processing/' + directoryName)    

#set up database
conn = sqlite3.connect('database/db.sqlite')
cur = conn.cursor()

#FOR TESTING ONLY
#cur.execute('''DROP TABLE IF EXISTS Members''')
#cur.execute('''DROP TABLE IF EXISTS Videos''')
#cur.execute('''DROP TABLE IF EXISTS Views''')

#cur.execute('''
#    ALTER TABLE Videos
#    ADD COLUMN genre TEXT	
# ''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Members
    (uid TEXT PRIMARY KEY,
     membership_id TEXT,
     alleg_account_id INTEGER,
     first_name TEXT,	
     last_name TEXT,
     email TEXT)	
 ''')
     
cur.execute('''
    CREATE TABLE IF NOT EXISTS Videos
    (media_id INTEGER PRIMARY KEY,	
     title TEXT,          
     content_channel TEXT,	
     video_length INTEGER,
     cid TEXT,
     genre TEXT)
 ''')
     
cur.execute('''
    CREATE TABLE IF NOT EXISTS Views
    (
    id INTEGER PRIMARY KEY,
    members_uid TEXT,
    videos_media_id INTEGER,
    date_time TEXT NOT NULL,
    date_seconds INTEGER NOT NULL,
    time_watched INTEGER,	
    device TEXT,
    CONSTRAINT unique_views UNIQUE (members_uid, videos_media_id, date_time)
    ) 
 ''')

#get last entry from Views
start = 0
cur.execute('SELECT max(id) FROM Views')
try:
    row = cur.fetchone()
    if row[0] is not None: start = row[0]
        
except:
    start = 0
    row = None


#parse csv files 

#lamda functions for data cleaning, using helpers from helpers.py
validateInteger = lambda x: helpers.validate_integer(x)
createAllegID = lambda x: helpers.create_alleg_id(x)
validateUID = lambda x: helpers.validate_uid(x)
validateMediaID = lambda x: helpers.validate_media_id(x)
validateDatetime = lambda x: helpers.validate_datetime(x)
dateToSeconds = lambda x: helpers.datetime_to_seconds(x)

commits = []

for file in toParse[:]:     
    print('\nPROCESSING DIRECTORY:', file) 
    
    directoryName = file.rstrip('.zip')
    pathToCsvFiles = 'processing/' + directoryName + '/KLRN/'
    csvFilePaths = glob.glob(os.path.join(pathToCsvFiles, '*.csv'))    
    
    for csvFilePath in csvFilePaths:
        csvFile = os.path.basename(csvFilePath)
        print('\tPROCESSING CSV FILE:', csvFile) 
    
        #don't bring in header since it might be in wrong location
        df = pd.read_csv(csvFilePath, header=None, keep_default_na=False,
                         on_bad_lines='skip', encoding='utf-8')
        
        #strip leading and trailing white spaces on all string data     
        for col in df.columns: 
            if df[col].dtype == object: df[col] = df[col].str.strip()
                
        #SET HEADER
        #find header and copy it   
        theHeader = df[df[0] == 'First Name'].values[0]
        #print(theHeader,'\n')
       
        #now remove the unused header    
        df = df[df[0] != 'First Name'] 
        
        #and replace the dataframe default with the copied header
        df.columns = theHeader
        
        #Sort by date and drop duplicate rows
        df = df.sort_values(by=['Date Watched'])
        df = df.drop_duplicates()
        
        
        #START VALIDATION    
        #validate UID as having 36 characters and four dashes
        df['UID'] = df['UID'].map(validateUID)
        
        #validate CID using validateUID filter
        df['CID'] = df['CID'].map(validateUID) 
        
        #VALIDATE INTEGERS    
        #validate Media ID as 9 or 10 digit integer
        df['TP Media ID'] = df['TP Media ID'].map(validateMediaID)
        
        #drop rows with invalid UIDs or Media IDs
        df = df[(df['UID'] != '') & (df['TP Media ID'] != 0)] 
        
        #validate Membership ID as valid integer, and slice it to create Alleg ID
        df['Alleg ID'] = df['Membership ID'].map(createAllegID)
    
        #validate Video Length as integer
        df['Total Run Time of the video'] = df['Total Run Time of the video'].map(validateInteger)
    
        #validate Time Watched as integer
        df['Time Watched'] = df['Time Watched'].map(validateInteger)  
        
        
        #VALIDATE EMAIL        
        #check that emails have @, replace with blank if not
        df['Email'] = np.where(df['Email'].str.contains('@'), df['Email'], '')
        
        
        #VALIDATE TIMES    
        #check that date_times at least have valid IS0-8601 date, replace with blank if not
        df['Date Watched'] = df['Date Watched'].map(validateDatetime)
        
        #create date only column, using seconds as an integer
        df['Date Seconds'] = df['Date Watched'].map(dateToSeconds) 
        
        #add empty Genre column if it doesn't exist
        if 'Genre' not in df.columns: df['Genre'] = ''   
       
        for index, row in df.iterrows(): 
            start += 1        
    
            #members table
            uid = row['UID']
            membership_id = row['Membership ID']  
            alleg_account_id = row['Alleg ID']    
            first_name = row['First Name'] 	
            last_name = row['Last Name']
            email = row['Email'] 
            
            if first_name == np.NaN: helpers.check.append(first_name)
            
            cur.execute('''
                INSERT INTO Members 
                (uid, membership_id, alleg_account_id, first_name, last_name, email) 
                  VALUES (:uid, NULLIF(:membership_id, ''), NULLIF(:alleg_account_id, -1),
                          NULLIF(:first_name, ''), NULLIF(:last_name, ''), NULLIF(:email, ''))
                    ON CONFLICT(uid) DO UPDATE SET 
                      membership_id=NULLIF(:membership_id, ''), 
                      alleg_account_id=NULLIF(:alleg_account_id, -1), 
                      first_name=NULLIF(:first_name, ''), 
                      last_name=NULLIF(:last_name, ''), 
                      email=NULLIF(:email, '')   
                ''', 
                {'uid': uid, 'membership_id': membership_id, 'alleg_account_id': alleg_account_id, 
                 'first_name': first_name, 'last_name': last_name, 'email': email})
            
            #print(first_name, last_name)        
            
            '''
            print(uid, ' : ', type(uid))
            print(membership_id, ' : ', type(membership_id))
            print(alleg_account_id, ' : ', type(alleg_account_id))
            print(first_name, ' : ', type(first_name)) 
            print(last_name, ' : ', type(last_name))
            print(email, ' : ', type(email))
            print()
            '''
            
            #videos table
            media_id = row['TP Media ID']  	
            title = row['Title']                 
            content_channel = row['Content Channel']  	
            video_length = row['Total Run Time of the video']
            cid = row['CID'] 
            genre = row['Genre']  
            
            cur.execute('''
                INSERT INTO Videos 
                (media_id, title, content_channel, video_length, cid, genre) 
                  VALUES (:media_id, NULLIF(:title, ''), NULLIF(:content_channel, ''), 
                          NULLIF(:video_length, -1), NULLIF(:cid, ''), NULLIF(:genre, ''))
                    ON CONFLICT(media_id) DO UPDATE SET
                      title=NULLIF(:title, ''),                                    
                      content_channel=NULLIF(:content_channel, ''), 
                      video_length=NULLIF(:video_length, -1),
                      cid=NULLIF(:cid, ''),
                      genre=NULLIF(:genre, '')
                ''', 
                {'media_id': media_id, 'title': title, 'content_channel': content_channel, 
                 'video_length': video_length, 'cid': cid, 'genre': genre}) 
                
            #print(title)    
            
            '''
            print(media_id, ' : ', type(media_id))
            print(title, ' : ', type(title))        
            print(content_channel, ' : ', type(content_channel))
            print(video_length, ' : ', type(video_length))
            print(cid, ' : ', type(cid))
            print(genre, ' : ', type(genre))
            print()
            ''' 
            
            #views table
            id = start #not using after all - auto incrementing instead   
            date_time = row['Date Watched']  
            date_seconds = row['Date Seconds']  
            time_watched = row['Time Watched']
            device = row['Device'] 
            
            cur.execute('''
                INSERT OR IGNORE INTO Views 
                (members_uid, videos_media_id, date_time, date_seconds, time_watched, device) 
                VALUES (NULLIF(?, ''), NULLIF(?, -1), NULLIF(?, ''), NULLIF(?, -1), NULLIF(?, -1), NULLIF(?, ''))''', 
                (uid, media_id, date_time, date_seconds, time_watched, device))
                
            #print(id)    
            #print(date_time)    
            
            '''        
            print(id, ' : ', type(id))
            print(date_time, ' : ', type(date_time))
            print(date_seconds, ' : ', type(date))
            
            print(datetime_to_string(date))
            print(time_to_string(time))
            
            print(time_watched, ' : ', type(time_watched))
            print(device, ' : ', type(device))
            print('================================\n')
            '''  
            
            #print('================================\n')
            
        #commit file
        conn.commit()
        
        #record results
        commits.append('FILE COMMITTED TO DATABASE: ' + csvFilePath) 
        df.to_csv('committed/' + directoryName + '-' + csvFile, 
                  index=False, encoding='utf-8-sig') 
        
conn.close()
database_backup('database/db.sqlite', 'database/archive/')
delete_old_backups('database/archive/', days_old=190)

print()
for commit in commits:
    print(commit)
