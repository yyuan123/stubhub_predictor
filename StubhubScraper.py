# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 15:29:22 2014

@author: dstuckey
"""

import urllib2
from bs4 import BeautifulSoup

baseUrl = 'http://www.stubhub.com/listingCatalog/select?'
nbaRegSeasonGenre = 81016

# ***edit to include date filter***
def constructEventQueryUrl():
    url = baseUrl + "q=stubhubDocumentType:event%20AND%20event_date:[NOW%20TO%20*]%20AND%20ancestorGenreIds:" + str(nbaRegSeasonGenre) + "&fl=event_id+description+ancestorGenreIds"
    return url

def constructTicketQueryUrl(eventId):
    url = baseUrl + "q=stubhubDocumentType:ticket%20AND%20event_id:" + str(eventId) + "&fl=curr_price+section+row_desc+seats+zonedesc"
    return url

eventQueryUrl = constructEventQueryUrl()
eventResponse = urllib2.urlopen(eventQueryUrl)
eventSoup = BeautifulSoup(eventResponse)

print eventQueryUrl

event_ids = eventSoup.findAll('str', {'name':'event_id'})
event_ids = [str(x.text) for x in event_ids]

print len(event_ids), " events found"

### For each event, pull available ticket info ###
#...

# ***Try just the first event***
firstTicketQuery = constructTicketQueryUrl(event_ids[0])
firstTicketResponse = urllib2.urlopen(firstTicketQuery)
ticketSoup = BeautifulSoup(firstTicketResponse)

print(firstTicketQuery)