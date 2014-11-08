# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 15:29:22 2014

@author: dstuckey
"""

import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import MySQLdb as myDB
from sqlalchemy import create_engine

baseUrl = 'http://www.stubhub.com/listingCatalog/select?'
nbaRegSeasonGenre = 81016
saveDir = './csvs'
mysql_user = "root"
mysql_pass = ""
mysql_db = "stubhub"

### Functions ###
def getDBConnect():
    return myDB.connect(host='localhost',
                                user=mysql_user,
                                passwd=mysql_pass,
                                db=mysql_db)

# Function to save DataFrame to MySQL database
def saveToDB(df, table, dbConnect, replace):
    if (replace):
        action='replace'
    else:
        action='append'
    #clean up any 'NaN' fields which mysql doesn't understand
    dfClean = df.where((pd.notnull(df)), None)
    dfClean.to_sql(con=dbConnect,
                    name=table,
                    if_exists=action,
                    flavor='mysql')

# Missing sqlalchemy.schema module
def readFromDB(termId, dbConnect):
    engine = create_engine('mysql+mysqldb://' + mysql_user + ':' + mysql_pass + '@localhost/' + mysql_db)
    
    df = pd.read_sql_table('sp_' + termId, con=engine)
    #clean up SUBJ column
    #df.SUBJ = df.SUBJ.str.strip()
    return df
    
# Get Current time formatted
def now():
    dt = datetime.datetime.now()
    return str(dt)

# Function to save a dataframe to CSV
def saveToCsv(df, name):
    df.to_csv(saveDir + '/' + name + '.csv')

# ***edit to include date filter***
def constructEventQueryUrl():
    url = baseUrl + "q=stubhubDocumentType:event%20AND%20event_date:[NOW%20TO%20*]%20AND%20ancestorGenreIds:" + str(nbaRegSeasonGenre) + "&fl=event_id+description+ancestorGenreIds+event_date"
    return url

def constructTicketQueryUrl(eventId):
    url = baseUrl + "q=stubhubDocumentType:ticket%20AND%20event_id:" + str(eventId) + "&fl=curr_price+section+row_desc+seats+zonedesc"
    return url
# 
def runTicketQuery(event_id):
    ticketQuery = constructTicketQueryUrl(event_id)
    firstTicketResponse = urllib2.urlopen(ticketQuery)
    ticketSoup = BeautifulSoup(firstTicketResponse)
    
    queryTime = now()

    #print(ticketQuery)
    prices = []
    sections = []
    seats = []
    zones = []
    rows = []
    eventIds = []
    queryTimes = []
    
    ticketDocs = ticketSoup.findAll('doc')
    for doc in ticketDocs:
        price = str(doc.find('float', {'name':'curr_price'}).text)[:63]
        prices.append(price)
        section = str(doc.find('str', {'name':'section'}).text)[:63]
        sections.append(section)
        seat = str(doc.find('str', {'name':'seats'}).text)[:63]
        seats.append(seat)
        zone = str(doc.find('str', {'name':'zonedesc'}).text)[:63]
        zones.append(zone)
        row = str(doc.find('str', {'name':'row_desc'}).text)[:63]
        rows.append(row)
        #add constant vals
        eventIds.append(eventId)
        queryTimes.append(queryTime)
    
    ticketDict = {
        'section': sections,
        'price': prices,
        'seats': seats,
        'zone': zones,
        'row': rows,
        'event_id': eventIds,
        'query_time': queryTimes
    }
    
    return pd.DataFrame(ticketDict)


### End Functions ###

#print eventQueryUrl

eventQueryUrl = constructEventQueryUrl()
eventResponse = urllib2.urlopen(eventQueryUrl)
eventSoup = BeautifulSoup(eventResponse)

eventIds = []
eventDates = []
eventDescriptions = []


eventDocs = eventSoup.findAll('doc')
for doc in eventDocs:
    eventId = str(doc.find('str', {'name':'event_id'}).text)
    eventIds.append(eventId)
    eventDesc = str(doc.find('str', {'name':'description'}).text)[:63]
    eventDescriptions.append(eventDesc)
    eventDate = str(doc.find('date', {'name':'event_date'}).text)[:63]
    eventDates.append(eventDate)
    
eventDict = {
    'event_id': eventIds,
    'date': eventDates,
    'description': eventDescriptions
}

eventDF = pd.DataFrame(eventDict)
#truncate 'description' column to 64 chars max
eventDF['description'] = eventDF['description'].str[:63]

saveToCsv(eventDF, 'upcoming_nba_games')

# previous method
#event_ids = eventSoup.findAll('str', {'name':'event_id'})
#event_ids = [str(x.text) for x in event_ids]
#print len(event_ids), " events found"

dbCon = getDBConnect()

### For each event, pull available ticket info ###
for i in range(0,len(eventDF)-1):
    event_id = eventDF['event_id'][i]
    ticketsDF = runTicketQuery(event_id)
    saveToCsv(ticketsDF, 'event_' + event_id + '_tickets')
    saveToDB(ticketsDF, "available_tickets", dbCon, replace=False)
