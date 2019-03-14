# Importing required modules
from pymongo import MongoClient
import time
import os
import sys
import logging

#Storing important data as log file
#logging.basicConfig(filename='/home/pi/Desktop/atc/evtm_log.log', level=logging.DEBUG, format= '%(asctime)s %(levelname)s:%(message)s')

#Connecting to Mongodb database
client = MongoClient('mongodb+srv://root:devashishbittu@cluster0-kckqv.mongodb.net/ATC?retryWrites=true&ssl=true&ssl_cert_reqs=CERT_NONE')
db = client.ATC
collection = db['ATC']
collection1 = db['EVTM']

#Updating current EVTM status in ATC databse
def update():
    #logging.info("Updating")
    #Query for updating
    result = collection.update_one(
        {"ID" : ID},
        {"$set" : {"EVTM" : EVTM}}
                        )
    #Saving important data to log file
    #logging.info(result.matched_count)
    #logging.info(result.modified_count)
    #logging.info("Finished updating data")

    #logging.info(db.collection_names(include_system_collections=False))
    #logging.info("Updated")
    pass

#Fetching Density data from ATC database
def fetch():
    #logging.info("Fetching")
    global ID
    global EVTM
    #Query for fetching
    UpdatedDocument = collection1.find_one({"POST_ID" : 1})
    ID=UpdatedDocument['POST_ID']
    EVTM=UpdatedDocument['LANE']
    print(ID)
    print(EVTM)
    #Saving important data to log file
    #logging.info("ID")
    #logging.info(ID)
    #logging.info("LANE")
    #logging.info(EVTM)
    #logging.info("Fetched")
    pass
    
#Infity loop for updating data
while(1):
    try:
        fetch()
        update()
        time.sleep(2)
    #Debugging any error if occured
    except Exception as e:
        #logging.info("Error Occurred!")
        print (e)
        pass
    




