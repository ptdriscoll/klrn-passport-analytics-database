# KLRN Passport Analytics Database 

This application cleans and parses PBS Passport viewing data, and stores results in a database. 

This allows searches on what viewers watch, when they watch and how much they watch on web TV and in online apps. Data searches can also be cross-referenced with membership data. PBS provides the data monthly, in a Zip file.

### Getting started

This works with Python 2.7 and the Python libraries NumPy and pandas. So make sure those are installed.   

After cloning the application to your working environment, open the app folder and add the monthly Passport Zip files to the downloads folder.  

Also in the app folder, open the db_process.py file. Under settings at the top, add all the Zip file names to the toParse list. 

For example:  

```python
#multiple files can be listed - important to seed start
toParse = [
    'KLRN_export_1_5_2017_all.zip',
    'KLRN_export_2_1_2017.zip',
    'KLRN_export_3_1_2017.zip',
    'KLRN_export_4_1_2017.zip',
    'KLRN_export_5_1_2017.zip',
    'KLRN_export_6_1_2017.zip',
    'KLRN_export_7_1_2017.zip'
] 
```

Also, just below this, delete or note out the repeated toParse list, like this:

```python
#this single override just updates the latest download 
#toParse = [
#    'KLRN_export_8_1_2017.zip'
#]  
```
  
Now save the changes to db_process.py, and run the file to create the database. 

This will also add a processing folder to handle Excel files pulled from the Zip files, and a committed folder to store those Excel files for reference.

### Searching the database

Upload the database into a SQLite-compatible editor or viewer. A nice, free option is DB Browser for SQLite (see link below). 

With DB Browser open, click the Open Database button at the top. In the file navigator that opens, go to app/database in the application and load db.sqlite.

Click the Browse Data tab to view, sort and filter the data tables. 

Click the Execute SQL tab to open an interface to run SQL queries. In the app folder, the files ref_queries.txt and ref_queries_members.txt provide some basic queries.

<br>

![](http://www.onthemoveblog.com/web-apps/images/Top_Channel_Views_v3.jpg)

### Visualizing data

To run visualizations, the Python library Matplotlib must be installed.  

In the app folder, the file queries_views_channels.py will search top content channels by dates. Set the search dates under settings at the top of the file.

Running the file will create an output_tables folder with a csv file of the results, and an output_graphics folder with a pie-chart of the top five channels.

### Cross-referencing membership data 

You will want to check the database's membership_id column in the Members table to make sure that these were extracted correctly. You will also need custom code to interact with downloads from you membership RMS (KLRN uses Allegiance).

In the app folder, the files queries_members_renewals.py and queries_members_segments.py show examples of how KLRN merges and segments viewer data with Excel files that have been placed in the members folder.

### Other files

These files store background functions:

- db_backup.py
- graphs.py
- helpers.py
- queries.py 

### References

- https://www.python.org/
- http://www.numpy.org/
- http://pandas.pydata.org/
- http://sqlitebrowser.org/
- http://matplotlib.org/