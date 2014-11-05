# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 15:29:22 2014

@author: dstuckey
"""

import urllib2
from bs4 import BeautifulSoup
import pandas as pd

baseUrl = 'http://www.stubhub.com/listingCatalog/select?'
nbaRegSeasonGenre = 81016
saveDir = './csvs'

### Functions ###
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

    #print(ticketQuery)
    prices = []
    sections = []
    seats = []
    zones = []
    rows = []
    
    ticketDocs = ticketSoup.findAll('doc')
    for doc in ticketDocs:
        price = str(doc.find('float', {'name':'curr_price'}).text)
        prices.append(price)
        section = str(doc.find('str', {'name':'section'}).text)
        sections.append(section)
        seat = str(doc.find('str', {'name':'seats'}).text)
        seats.append(seat)
        zone = str(doc.find('str', {'name':'zonedesc'}).text)
        zones.append(zone)
        row = str(doc.find('str', {'name':'row_desc'}).text)
        rows.append(row)
    
    ticketDict = {
        'section': sections,
        'price': prices,
        'seats': seats,
        'zone': zones,
        'row': rows
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
    eventDesc = str(doc.find('str', {'name':'description'}).text)
    eventDescriptions.append(eventDesc)
    eventDate = str(doc.find('date', {'name':'event_date'}).text)
    eventDates.append(eventDate)
    
eventDict = {
    'event_id': eventIds,
    'date': eventDates,
    'description': eventDescriptions
}

eventDF = pd.DataFrame(eventDict)

saveToCsv(eventDF, 'upcoming_nba_games')

# previous method
#event_ids = eventSoup.findAll('str', {'name':'event_id'})
#event_ids = [str(x.text) for x in event_ids]
#print len(event_ids), " events found"

### For each event, pull available ticket info ###
for i in range(0,5):
    event_id = eventDF['event_id'][i]
    ticketsDF = runTicketQuery(event_id)
    saveToCsv(ticketsDF, 'event_' + event_id + '_tickets')
