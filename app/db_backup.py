# -*- coding: utf-8 -*-

import os, errno
import datetime
import sqlite3
import shutil
import time


#back up database using update step and datetime stamp in name
def database_backup(db, backup_dir, step=''):
    
    #create backup_dir if it doesn't exist
    try:
        os.makedirs(backup_dir)
    except OSError as e:
        if e.errno != errno.EEXIST: raise                
    
    #create output_path with update step and datetime stamps in name
    if len(step) > 0:
        step = '_' + step
    date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 
    output_file = '{}'.format(date) + step + '.sqlite'
    output_path = os.path.join(backup_dir, output_file)

    conn = sqlite3.connect(db)
    cur = conn.cursor()
    
    #lock database from any writes or updates
    cur.execute('BEGIN EXCLUSIVE')

    shutil.copyfile(db, output_path)

    #unlock database
    conn.rollback()
    conn.close()
    
    print '\nDATABASE BACKED UP:', os.path.basename(output_path)

def delete_old_backups(backup_dir, days_old=90):
    print ''
    deletions = False
    cutoff_days = time.time() - days_old * 86400
    
    #loop through files in backup_dir
    for fname in os.listdir(backup_dir):
        pname = os.path.join(backup_dir, fname)        
        
        #remove files older than days_old
        if os.path.isfile(pname):            
            if os.stat(pname).st_ctime < cutoff_days:
                deletions = True
                os.remove(pname)
                print 'BACKUP DATABASE DELETED:', os.path.basename(pname)
                
    if not deletions: print 'NO BACKUP DATABASES DELETED'