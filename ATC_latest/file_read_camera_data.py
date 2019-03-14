import os
import time
from pymongo import MongoClient

traffic_post_id = "TP1"


connection_status = True
while (connection_status):
	try:
		print("Connecting......")
		conn  = MongoClient('mongodb+srv://root:devashishbittu@cluster0-kckqv.mongodb.net/TEST?retryWrites=true&ssl=true&ssl_cert_reqs=CERT_NONE')
		#conn1 = MongoClient('mongodb://devparseuser:dev2486fparse1ewgFHFEGH@18.222.143.35/isdr-dev-db')
		print("Connected successfully!!!")
		db = conn.TEST
		#db1 = conn1['isdr-dev-db']
		traffic_post_collection = db.TRAFFIC_POST
		density_collection = db.DENSITY
		connection_status = False

	except Exception as e:
		print(e)
		print("Could not connect to MongoDB. Trying again!")
		time.sleep(10)

def data_fetch(data_status=True):
    while(data_status):
        data = ""
        try:
            file = open("mytest1.txt","r")
            for line in file:
                data = line
            file.close()
            data_status = False
            return data

        except Exception as e:
            print(e)
            data_status = True

while(1):
	text = data_fetch()
	if(text == ""):
		print("Data not found!")
		continue
	else:
		data = ""
		Value = []
		temp = list(text)
		for i in range(1,len(temp)):
		    if ((temp[i] == ',') or (temp[i] == ']')):
		        Value.append(int(data))
		        data = ""
		        continue
		    data = data + temp[i]
		print("Value:",Value)
	density_value = sum(Value)/50
	print("Density:",density_value)
	result = density_collection.update_one({"density_id_PK" : "L1"}, {"$set" : {"density" : density_value}})


