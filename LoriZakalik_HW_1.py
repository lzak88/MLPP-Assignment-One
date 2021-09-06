# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 10:39:39 2021

@author: loriz
"""


import pandas as pd
import requests
import json
import psycopg2


#Functions

#Function to convert state code 36 to the state abbreviation
def stateName(s):
    if s == '36':
        return 'NY'
    

#Convert county fips code to county name
def countyName(c):
    if c == '001':
        return 'Albany County'
    elif c == '003':
        return 'Allegany County'
    elif c == '005':
        return 'Bronx County'
    elif c == '007':
        return 'Broome County'
    elif c == '009':
        return 'Cattaraugus County'
    elif c == '011':
        return 'Cayuga County'
    elif c == '013':
        return 'Chautauqua County'
    elif c == '015':
        return 'Chemung County'
    elif c == '017':
        return 'Chenango County'
    elif c == '019':
        return 'Clinton County'
    elif c == '021':
        return 'Columbia County'
    elif c == '023':
        return 'Cortland County'
    elif c == '025':
        return 'Delaware County'
    elif c == '027':
        return 'Dutchess County'
    elif c == '029':
        return 'Erie County'
    elif c == '031':
        return 'Essex County'
    elif c == '033':
        return 'Franklin County'
    elif c == '035':
        return 'Fulton County'
    elif c == '037':
        return 'Genesee County'
    elif c == '039':
        return 'Greene County'
    elif c == '041':
        return 'Hamilton County'
    elif c == '043':
        return 'Herkimer County'
    elif c == '045':
        return 'Jefferson County'
    elif c == '047':
        return 'Kings County'
    elif c == '049':
        return 'Lewis County'
    elif c == '051':
        return 'Livingston County'
    elif c == '053':
        return 'Madison County'
    elif c == '055':
        return 'Monroe County'
    elif c == '057':
        return 'Montgomery County'
    elif c == '059':
        return 'Nassau County'
    elif c == '061':
        return 'New York County'
    elif c == '063':
        return 'Niagra County'
    elif c == '065':
        return 'Oneida County'
    elif c == '067':
        return 'Onondaga County'
    elif c == '069':
        return 'Ontario County'
    elif c == '071':
        return 'Orange County'
    elif c == '073':
        return 'Orleans County'
    elif c == '075':
        return 'Oswego County'
    elif c == '077':
        return 'Otsego County'
    elif c == '079':
        return 'Putnam County'
    elif c == '081':
        return 'Queens County'
    elif c == '083':
        return 'Rensselaer County'
    elif c == '085':
        return 'Richmond County'
    elif c == '087':
        return 'Rockland County'
    elif c == '089':
        return 'St. Lawrence County'
    elif c == '091':
        return 'Saratoga County'
    elif c == '093':
        return 'Schenectady County'
    elif c == '095':
        return 'Shoharie County'
    elif c == '097':
        return 'Schuyler County'
    elif c == '099':
        return 'Seneca County'
    elif c == '101':
        return 'Steuben County'
    elif c == '103':
        return 'Suffolk County'
    elif c == '105':
        return 'Sullivan County'
    elif c == '107':
        return 'Tioga County'
    elif c == '109':
        return 'Tompkins County'
    elif c == '111':
        return 'Ulster County'
    elif c == '113':
        return 'Warren County'
    elif c == '115':
        return 'Washington County'
    elif c == '117':
        return 'Wayne County'
    elif c == '119':
        return 'Westchester County'
    elif c == '121':
        return 'Wyoming County'
    elif c == '123':
        return 'Yates County'  
    else:
        return 'N/A'


#converts a dataframe to a csv file
def DFtoCSV(df, filename):
    df.to_csv(filename)

#converts a csv file to a list of lists
def csvToList(filename):
    with open('pop_data_final.csv', 'r') as fin:
        new_list = []
        for line in fin:
            new_line = line.strip().split(',')
            if len(new_line) > 0:
                new_list.append(new_line)
    return new_list[1:]

#main program
def main():
    #my api key acquired during my summer internship
    apiKey = "b03f25834ad3b3bd1f1607d84a78976e3d477733"

    host = 'https://api.census.gov/data'
    year = '2019'
    dataset = 'acs/acs5'
    base_url = '/'.join([host, year, dataset])
    
    #empty dictionary to store URL info
    predicates = {}
    
    #these are the variables I am pulling from the ACS
    get_vars = ['NAME', 'B01003_001E','B19013_001E','B01001_002E','B01001_026E','B02001_002E',
        'B02001_003E','B02001_005E','B02001_007E','B02001_008E']
    
    #storing URL info in predicates dictionary
    predicates['get'] = ','.join(get_vars)
    predicates['for'] = 'block group:*'
    predicates['in'] = 'state:36;county:*'
    predicates['key'] = apiKey

    req = requests.get(base_url, params = predicates)

    #renaming columns
    col_names = ['GeoName', 'Total Pop', 'Median Inc', 'Pop Male', 'Pop Female', 'Pop White',
             'Pop Black', 'Pop Asian', 'Pop Other', 'Pop Multi Race', 'State Code', 'County Code', 
             'Tract', 'Block Group']

    #Converting census data into dataframe
    pop_data = pd.DataFrame(columns = col_names, data = req.json()[1:])

    #Data cleaning / adjusting any outliers
    pop_data['Total Pop'] = pop_data['Total Pop'].astype(int)
    pop_data['Median Inc'] = pop_data['Median Inc'].astype(int)
    pop_data['Pop Male'] = pop_data['Pop Male'].astype(int)
    pop_data['Pop Female'] = pop_data['Pop Female'].astype(int)
    pop_data['Pop White'] = pop_data['Pop White'].astype(int)
    pop_data['Pop Black'] = pop_data['Pop Black'].astype(int)
    pop_data['Pop Asian'] = pop_data['Pop Asian'].astype(int)
    pop_data['Pop Other'] = pop_data['Pop Other'].astype(int)
    pop_data['Pop Multi Race'] = pop_data['Pop Multi Race'].astype(int)

    #taking a high end look at the data.
    pop_data.describe()
    
    #Adjusting negative median incomes
    pop_data['Median Inc'][pop_data['Median Inc'] < 0] = 0
    
    #adding a column with state name
    pop_data['State Name'] = pop_data['State Code'].apply(stateName)
   
    #adding a column with county name
    pop_data['County Name'] = pop_data['County Code'].apply(countyName)

    #removing the column with all geographies now that we have individual columns for each              
    pop_data = pop_data.drop('GeoName', 1) 

    pop_data = pop_data[['State Name', 'County Name', 'Total Pop', 'Median Inc', 'Pop Male', 'Pop Female', 'Pop White',
             'Pop Black', 'Pop Asian', 'Pop Other', 'Pop Multi Race', 'State Code', 'County Code', 
             'Tract', 'Block Group']]
  
    #checking that data loaded
    print(pop_data.head())

    #downloading data as csv
    file = 'pop_data_final.csv'
    #calling dataframe to CSV function
    DFtoCSV(pop_data, file)

    #calling csv to list function
    acs_data = csvToList(file)

    #connecting to database
    connection = psycopg2.connect(user='mlpp_student', password='CARE-horse-most', 
                              host='acs-db.mlpolicylab.dssg.io', port='5432', database='acs_data_loading')
    cursor = connection.cursor()

    #dropping table because I've run script a few times
    table_drop = '''DROP TABLE IF EXISTS acs.lzakalik_acs_data'''
    cursor.execute(table_drop)
    
    #creating table
    table = """CREATE TABLE IF NOT EXISTS acs.lzakalik_acs_data (
                ID INTEGER PRIMARY KEY,
                STATE_NAME VARCHAR,
                COUNTY_NAME VARCHAR,
                TOTAL_POP INTEGER,
                MEDIAN_INC INTEGER,
                MALE_POP INTEGER,
                FEMALE_POP INTEGER,
                WHITE_POP INTEGER,
                BLACK_POP INTEGER,
                ASIAN_POP INTEGER,
                OTHER_POP INTEGER,
                MULTI_RACE_POP INTEGER,
                STATE_CODE VARCHAR,
                COUNTY_CODE VARCHAR,
                TRACT VARCHAR,
                BLOCK_GROUP VARCHAR);"""
    
    cursor.execute(table)
    print("Table created successfully")
    connection.commit()
    
    #inserting data into table
    sql_insert = '''INSERT INTO acs.lzakalik_acs_data (ID, STATE_NAME, COUNTY_NAME, TOTAL_POP, MEDIAN_INC, MALE_POP, FEMALE_POP, WHITE_POP, 
                                                    BLACK_POP, ASIAN_POP, OTHER_POP, MULTI_RACE_POP,
                                                    STATE_CODE, COUNTY_CODE, TRACT, BLOCK_GROUP) 
                                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                                    %s,%s,%s,%s,%s,%s)'''

    cursor.executemany(sql_insert, acs_data)
    connection.commit()

    #testing to confirm data is there
    test = 'SELECT * FROM acs.lzakalik_acs_data';
    cursor.execute(test)
    acs_table = cursor.fetchall()

    acs_table_df = pd.DataFrame(acs_table, columns = [name[0] for name in cursor.description])
    print(acs_table_df.head)
    print(acs_table_df.tail)
    
    connection.close()

if __name__ == '__main__':
    main()