# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
import re 


'''
validattion helpers
'''

#precompiled regexes
numbersRegex = re.compile(r'^[0-9]+$') #check for numbers only
zerosRegex = re.compile(r'^[0]+$') #check for zeros only

def validate_integer(d):
    if pd.notnull(d) and numbersRegex.search(d) is not None: 
        return int(d)
    return -1

#validate Membership ID as valid integer that's not 0, and then slice it to create Alleg ID
def create_alleg_id(d):
    if zerosRegex.search(d): 
        return -1         
    if pd.notnull(d) and numbersRegex.search(d) is not None: 
        n = int(d[2:])
        if len(str(n)) < 5: return -1 
        return n
    return -1

def validate_uid(s):
    if pd.notnull(s): 
        checkCharacters = len(s)
        checkDashes = len(s.split('-'))        
        if checkCharacters == 36 and checkDashes == 5: 
            return s
    return '' 
    
def validate_media_id(d):
    if pd.notnull(d):
        checkNumbers = numbersRegex.search(d)
        checkCharacters = len(d)
        if checkNumbers and (checkCharacters == 9 or checkCharacters == 10):
            return int(d)
    return -1          

'''
datetime helpers
'''

#checks that a string is in IS0-8601 datetime format
def validate_datetime(d, format='%Y-%m-%d %H:%M:%S'):
    try:      
        check = datetime.strptime(d.split('+')[0].split('.')[0], format)
        return d
    except:
        return ''    
        
#oonvert IS0-8601 datetime string to unix seconds integer
def datetime_to_seconds(d, format='%Y-%m-%d %H:%M:%S'): 
    try:        
        if len(d) < 1:
            return -1  
        unix = datetime(1970, 1, 1, 0, 0, 0 )
        check = datetime.strptime(d.split('+')[0].split('.')[0], format)
        return int((check - unix).total_seconds())
    except:
        return -1

#oonvert unix seconds to datetime string in UTC - IS0-8601 is default format
def datetime_to_string(d, format='%Y-%m-%d %H:%M:%S'):
    return datetime.utcfromtimestamp(d).strftime(format)

'''
time only helpers
'''    

#precompiled default regex for timeToSeconds function
timeRegex = re.compile(r'([0-9][0-9]:[0-9][0-9]:[0-9][0-9])(\.[0-9]+)?') 

#oonvert just time from IS0-8601 string to seconds float
def time_to_seconds(t, regex=timeRegex):
    try:
        check = re.search(regex, t)
        time = check.group(1).split(':')  
        millesec = float(check.group(2)) if check.group(2) else 0
        return float(time[0])*60*60 + float(time[1])*60 + float(time[2]) + millesec
    except:
        return float(-1)
        
#oonvert seconds to hrs, mins, secs, microsecs - IS0-8601 default format
def time_to_string(t, format='%H:%M:%S'):
    return datetime.utcfromtimestamp(t).strftime(format)