# -*- coding: utf-8 -*-


# Python code to illustrate
# inserting data in MongoDB

from pymongo import MongoClient
import json
# pprint library is used to make the output look more pretty from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connecti-kckqv.mongodb.net:

#conn  = MongoClient('mongodb://root:devashishbittu@cluster0-shard-00-00-kckqv.mongodb.net:27017,cluster0-shard-00-01-kckqv.mongodb.net:27017,cluster0-shard-00-02-kckqv.mongodb.net:27017/TDMC?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
#db = conn.TDMC
try:
    
  #  serverStatusResult=db.command("serverStatus")
  #  pprint(serverStatusResult)
	conn  = MongoClient('mongodb+srv://root:devashishbittu@cluster0-kckqv.mongodb.net/TEST?retryWrites=true&ssl=true&ssl_cert_reqs=CERT_NONE')
	print("Connected successfully!!!")
	db = conn.TEST
	traffic_post_collection = db.TRAFFIC_POST
	gps_collecttion= db.GPS
	lane_collection = db.LANE
	device_collection = db.DEVICE
	vehicle_collection = db.VEHICLE
	construction_collection = db.CONSTRUCTION
	accident_collection = db.ACCIDENT
	fire_collection = db.FIRE
	evtm_collection = db.EVTM
	pollution_collection = db.POLLUTION
	density_collection = db.DENSITY
except:  
    print("Could not connect to MongoDB. Trying again!")
    exit(0)
    
#try:
 #   conn = MongoClient()
  #  print("Connected successfully!!!")
#except:  
 #   print("Could not connect to MongoDB")
    
# database

lane = []
gps = []
device_name = []

def create_new_traffic_post(traffic_post_id):
	query = {"post_id_PK":traffic_post_id, "device":lane, "device_gps_id":gps}
	print(query)
	traffic_post_collection.insert_one(query)
	result = traffic_post_collection.find_one({"post_id_PK":traffic_post_id})
	return result

def create_new_gps(doc):
	gps_id = doc['device_gps_id']
	for i in range(0,len(gps_id)):
		query = {"post_id_PK": doc['_id'], "gps_id_PK": str(gps_id[i]), "gps_x":22.2458211, "gps_y":84.8941206}
		print(query)
		gps_collecttion.insert_one(query)

def create_new_device(doc):
	device_id = doc['device']
	for i in range(0,len(device_id)):
		query = {"post_id_PK": doc['_id'], "device_id_PK": str(device_id[i]), "device_name":device_name[i] + "_" + str(i)}
		print(query)
		device_collection.insert_one(query)

def create_new_lane_details(doc, city):
	device_id = doc['device']
	for i in range(0,len(device_id)):
		query = {"post_id_PK": doc['_id'], "lane_id_PK": device_id[i], "lane_name":"Rourkela_Sector1", "lane_area":20, "city": city}
		print(query)
		lane_collection.insert_one(query)

def create_new_vehicle_details(doc):
	device_id = doc['device']
	for i in range(0,len(device_id)):
		query = {"post_id_PK": doc['_id'], "vehicle_id_PK": device_id[i], "vehicle_count": 20, "people_count" :10}
		print(query)
		vehicle_collection.insert_one(query)

def create_new_density_details(doc):
	device_id = doc['device']
	for i in range(0,len(device_id)):
		query = {"post_id_PK": doc['_id'], "density_id_PK": device_id[i], "density":20, "time":30}
		print(query)
		density_collection.insert_one(query)


def main():
	traffic_post_id = str(input("Enter traffic post id: \n"))

	result = traffic_post_collection.find_one({"post_id_PK":traffic_post_id})
	if result:
		print("Already present in database.\n")
		exit(0)

	city = str(input("Enter the city: \n"))

	no_of_lanes = int(input("Enter number of lanes: \n"))

	for i in range(0,no_of_lanes):
		lane.append(str(input("Enter lane id: \n")))
		gps.append(str(input("Enter gps id: \n")))
		device_name.append(str(input("Enter device name: \n")))
		

	doc = create_new_traffic_post(traffic_post_id)
	create_new_gps(doc)
	create_new_device(doc)
	create_new_lane_details(doc, city)
	if traffic_post_id != "NILL":
		create_new_vehicle_details(doc)
		create_new_density_details(doc)

if __name__ == '__main__':
    main()




