from pymongo import MongoClient
import time
import os
import logging

logging.basicConfig(filename='/home/pi/atc-module/algo.log')

connection_status = True
while (connection_status):
	try:
		logging.warning("Connecting......")
		conn  = MongoClient('mongodb+srv://root:devashishbittu@cluster0-kckqv.mongodb.net/TEST?retryWrites=true&ssl=true&ssl_cert_reqs=CERT_NONE', connectTimeoutMS=5000, serverSelectionTimeoutMS=5000, socketTimeoutMS=5000)
		conn1 = MongoClient('mongodb://devparseuser:dev2486fparse1ewgFHFEGH@18.222.143.35/isdr-dev-db', connectTimeoutMS=5000, serverSelectionTimeoutMS=5000, socketTimeoutMS=5000)
		logging.warning("Connected successfully!!!")
		db = conn.TEST
		db1 = conn1['isdr-dev-db']
		tdmc_collection = db1.SCTdmc
		traffic_post_collection = db.TRAFFIC_POST
		density_collection = db.DENSITY
		connection_status = False

	except Exception as e:
		logging.warning(e)
		logging.warning("Could not connect to MongoDB. Trying again!")
		os.system("touch data.txt")
		os.remove("data.txt")
		file = open("data.txt", "w")
		file.write("Error")
		file.close()
		time.sleep(10)

#Time required for a traffic post cycle
fixed_time=2*60.00
threshold = 0.5


traffic_post_id = "TP1"

def fetch_density():
	result = traffic_post_collection.find({"post_id_PK": traffic_post_id} , {'_id':0, 'device':1})
	for record in result:
		lane = record['device']
	density = []
	for i in range(len(lane)):
		result = density_collection.find({'density_id_PK': lane[i]} , {'_id':0 , 'density':1})
		for record in result:
			density.append(record['density'])
	logging.warning(density)
	time_algorithm(density,lane)
	return lane

def time_algorithm(density,lane):
	time = []
	total_density = sum(density)
	result = all(i < threshold for i in density)
	if result:
		for z in range(len(density)):
			time.append(int(fixed_time/len(density)))
	else:	
		for z in range(len(density)):
			time.append(int((density[z]/total_density)*fixed_time))
	time_update(density,time,lane)

def time_update(density,time,lane):
	os.system("touch data.txt")
	os.remove("data.txt")
	file = open("data.txt", "w")
	file.write(str(time))
	#file.write(str(lane))
	for i in range(len(time)):
		result = density_collection.update_one({"density_id_PK" : lane[i]}, {"$set" : {"time" : time[i]}})
		lane = "lane"+str(i+1)
		result = tdmc_collection.update_one({"lane" : lane}, {"$set" : {"tdmcValue" : density[i]}})
		result = tdmc_collection.update_one({"lane" : lane}, {"$set" : {"timeSlot" : time[i]}})
	file.close()


if __name__ == '__main__':
	while(1):
		try:
			logging.warning("Starting!")
			start_time = time.time()
			lane = fetch_density()
			logging.warning("Execution time: ", time.time() - start_time, " sec")
			for i in range(len(lane)):
				result = density_collection.find({'density_id_PK': lane[i]} , {'_id':0 , 'time':1})
				for record in result:
					logging.warning("Lane "+ str(i+1)+ ": " + str(record['time']))
		except Exception as e:
			logging.warning(e)
			logging.warning("Error Occured!")
			logging.warning("Connecting Again!")
			os.system("touch data.txt")
			os.remove("data.txt")
			file = open("data.txt", "w")
			file.write("Error")
			file.close()
