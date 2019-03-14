# -*- coding: utf-8 -*-


# Python code to illustrate
# inserting data in MongoDB

from pymongo import MongoClient
import urllib.parse
from pprint import pprint
# pprint library is used to make the output look more pretty from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connecti-kckqv.mongodb.net:

#conn  = MongoClient('mongodb://root:devashishbittu@cluster0-shard-00-00-kckqv.mongodb.net:27017,cluster0-shard-00-01-kckqv.mongodb.net:27017,cluster0-shard-00-02-kckqv.mongodb.net:27017/TDMC?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
#db = conn.TDMC
try:
    
  #  serverStatusResult=db.command("serverStatus")
  #  pprint(serverStatusResult)
    conn  = MongoClient('mongodb://root:devashishbittu@cluster0-shard-00-00-kckqv.mongodb.net:27017,cluster0-shard-00-01-kckqv.mongodb.net:27017,cluster0-shard-00-02-kckqv.mongodb.net:27017/TDMC?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
    print("Connected successfully!!!")
except:  
    print("Could not connect to MongoDB. Trying again!")
    
#try:
 #   conn = MongoClient()
  #  print("Connected successfully!!!")
#except:  
 #   print("Could not connect to MongoDB")
    
# database

db = conn.TDMC
# Created or Switched to collection names: my_gfg_collection


c1= db.TBL_STG_2_SENS_GPS
c2 = db.TBL_STG_1_SENS_LANE
c3 = db.TBL_STG_3_SENS_DEVICE
c4 = db.TBL_STG_4_SENS_VEHICLE
c5 = db.TBL_STG_5_SENS_CONSTRUCTION
c6 = db.TBL_STG_6_SENS_ACCIDENT
c7 = db.TBL_STG_7_SENS_FIRE
c8 = db.TBL_STG_8_SENS_EVTM
c9 = db.TBL_STG_9_SENS_WEATHER
c10 = db.TBL_STG_10_SENS_DENSITY


 


e1 =(
     
       { "gps_id_PK":"G1", "gps_x":22.2458211, "gps_y":84.8941206},
       { "gps_id_PK":"G2", "gps_x":22.2500845, "gps_y":84.8853956},
       { "gps_id_PK":"G3", "gps_x":22.2517735, "gps_y":84.8763365},
       { "gps_id_PK":"G4", "gps_x":22.2457478, "gps_y":84.8737311,},
       { "gps_id_PK":"G5", "gps_x":22.24558399999999, "gps_y":84.86851999999999},
       { "gps_id_PK":"G6", "gps_x":22.244323899999998, "gps_y":84.85816559999999},
       { "gps_id_PK":"G7", "gps_x":22.25095259999999, "gps_y":84.8502772},
       { "gps_id_PK":"G8", "gps_x":22.250705399999998, "gps_y":84.84245709999999},
       { "gps_id_PK":"G9", "gps_x":22.24298700000000, "gps_y":84.8333322},
       { "gps_id_PK":"G10", "gps_x":22.231073400000003, "gps_y":84.9338081},
       

)


e2 = (
        {"lane_id_PK":"L1",  "lane_name":"Rourkela_Sector1","gps_id_FK":"G1", "lane_area":20},
        {"lane_id_PK":"L2",  "lane_name":"Rourkela_Sector2","gps_id_FK":"G2", "lane_area":30},
        {"lane_id_PK":"L3",  "lane_name":"Rourkela_Sector3","gps_id_FK":"G3", "lane_area":40},
        {"lane_id_PK":"L4",  "lane_name":"Rourkela_Sector4","gps_id_FK":"G4", "lane_area":50},
        {"lane_id_PK":"L5",  "lane_name":"Rourkela_Sector5","gps_id_FK":"G5", "lane_area":10},
        {"lane_id_PK":"L6",  "lane_name":"Rourkela_Sector6","gps_id_FK":"G6", "lane_area":30},
        {"lane_id_PK":"L7",  "lane_name":"Rourkela_Sector7","gps_id_FK":"G7", "lane_area":20},
        {"lane_id_PK":"L8",  "lane_name":"Rourkela_Sector8","gps_id_FK":"G8", "lane_area":50},
        {"lane_id_PK":"L9",  "lane_name":"Rourkela_Sector9","gps_id_FK":"G9", "lane_area":60},
        {"lane_id_PK":"L10",  "lane_name":"Rourkela_Sector10","gps_id_FK":"G10", "lane_area":30},
        
)


e3 = (
        {"device_id_PK":"d1", "gps_id_FK":"G1"},
        {"device_id_PK":"d2", "gps_id_FK":"G2"},
        {"device_id_PK":"d3", "gps_id_FK":"G3"},
        {"device_id_PK":"d4", "gps_id_FK":"G4"},
        {"device_id_PK":"d5", "gps_id_FK":"G5"},
        {"device_id_PK":"d6", "gps_id_FK":"G6"},
        {"device_id_PK":"d7", "gps_id_FK":"G7"},
        {"device_id_PK":"d8", "gps_id_FK":"G8"},
        {"device_id_PK":"d9", "gps_id_FK":"G9"},
        {"device_id_PK":"d10", "gps_id_FK":"G10"},
        
        )



e4 = (
        {"vehicle_id_PK":"v1", "vehicle_count": 20, "people_count" :10, "device_id_FK":"d1"},
        {"vehicle_id_PK":"v1", "vehicle_count": 10, "people_count" :20, "device_id_FK":"d2"},
        {"vehicle_id_PK":"v1", "vehicle_count": 30, "people_count" :30, "device_id_FK":"d3"},
        {"vehicle_id_PK":"v1", "vehicle_count": 40, "people_count" :40, "device_id_FK":"d4"},
        {"vehicle_id_PK":"v1", "vehicle_count": 30, "people_count" :50, "device_id_FK":"d5"},
        {"vehicle_id_PK":"v1", "vehicle_count": 20, "people_count" :20, "device_id_FK":"d6"},
        {"vehicle_id_PK":"v1", "vehicle_count": 10, "people_count" :30, "device_id_FK":"d7"},
        {"vehicle_id_PK":"v1", "vehicle_count": 50, "people_count" :40, "device_id_FK":"d8"},
        {"vehicle_id_PK":"v1", "vehicle_count": 60, "people_count" :20, "device_id_FK":"d9"},
        {"vehicle_id_PK":"v1", "vehicle_count": 70, "people_count" :10, "device_id_FK":"d10"},
        
        
        
        )
        

e5 =(
     
      {  "construction_loc_PK":"cnl1", "construction_req_time": 2, "construction_effected_area":20, "gps_id_FK":"G1"},
      {  "construction_loc_PK":"cnl2", "construction_req_time": 2, "construction_effected_area":20, "gps_id_FK":"G2"},
      {  "construction_loc_PK":"cnl3", "construction_req_time": 3, "construction_effected_area":30, "gps_id_FK":"G3"},
      {  "construction_loc_PK":"cnl4", "construction_req_time": 1, "construction_effected_area":10, "gps_id_FK":"G4"},

)


e6 = (
        {"accident_id_PK":"ad1", "accident_volume":10,"gps_id_FK":"G1"},
        {"accident_id_PK":"ad2", "accident_volume":20,"gps_id_FK":"G2"},
        {"accident_id_PK":"ad3", "accident_volume":30,"gps_id_FK":"G3"},
        {"accident_id_PK":"ad1", "accident_volume":40,"gps_id_FK":"G4"},
        
        
        )

e7 = (
       { "fire_id_PK":"sh1", "fire_volume": 20, "gps_id_FK":"G3"},

     )

e8 =(
        {"evtm_id_PK":"ev1", "evtm_source_FK":"L1","evtm_destination_FK":"L2"},
        {"evtm_id_PK":"ev2", "evtm_source_FK":"L3","evtm_destination_FK":"L4"},
    )

e9 = (
       { "weather_id_PK":"w1","weather_volume":10,"gps_id_FK":"G1"},
       { "weather_id_PK":"w2","weather_volume":20,"gps_id_FK":"G2"},
       { "weather_id_PK":"w3","weather_volume":30,"gps_id_FK":"G3"},
       { "weather_id_PK":"w4","weather_volume":40,"gps_id_FK":"G4"},
       { "weather_id_PK":"w5","weather_volume":10,"gps_id_FK":"G5"},
       { "weather_id_PK":"w6","weather_volume":20,"gps_id_FK":"G6"},
       { "weather_id_PK":"w7","weather_volume":30,"gps_id_FK":"G7"},    
       { "weather_id_PK":"w8","weather_volume":40,"gps_id_FK":"G8"},   
       { "weather_id_PK":"w9","weather_volume":10,"gps_id_FK":"G9"},
       { "weather_id_PK":"w10","weather_volume":20,"gps_id_FK":"G10"},
       
       
        )

e10 = (
       { "Traffic_density_PK":"T1", "gps_id_FK":"G1","density_value":10},
       { "Traffic_density_PK":"T2", "gps_id_FK":"G2","density_value":20},
       { "Traffic_density_PK":"T3", "gps_id_FK":"G3", "density_value":30},
       { "Traffic_density_PK":"T4", "gps_id_FK":"G4", "density_value":50},
       { "Traffic_density_PK":"T5", "gps_id_FK":"G5", "density_value":50},
       { "Traffic_density_PK":"T6", "gps_id_FK":"G6", "density_value":70},
       { "Traffic_density_PK":"T7", "gps_id_FK":"G7", "density_value":80},
       { "Traffic_density_PK":"T8", "gps_id_FK":"G8", "density_value":10},
       { "Traffic_density_PK":"T9", "gps_id_FK":"G9", "density_value":  30},
       { "Traffic_density_PK":"T10", "gps_id_FK":"G10", "density_value": 40},

)

 
# Insert Data
r1 = c1.insert_many(e1)
r2 = c2.insert_many(e2)
r3 = c3.insert_many(e3)
r4 = c4.insert_many(e4)
r5 = c5.insert_many(e5)
r6 = c6.insert_many(e6)
r7 = c7.insert_many(e7)
r8 = c8.insert_many(e8)
r9 = c9.insert_many(e9)
r10 = c10.insert_many(e10)

print("Data inserted with record ids",r1," ",r2," ",r3," ",r4," ",r5," ",r6," ",r7," ",r8," ",r9," ",r10,)
#print("Data inserted with record ids",r1,"  ",r2, " ",r3," ",r4)
#print("Data inserted with record ids",r6)
# Printing the data inserted
cursor = c1.find()
for record in cursor:
    print(record)
 
    
cursor = c2.find()
for record in cursor:
    print(record)
    
cursor = c3.find()
for record in cursor:
    print(record)
    
cursor = c4.find()
for record in cursor:
    print(record)

cursor = c5.find()
for record in cursor:
    print(record)
    
cursor = c6.find()
for record in cursor:
    print(record)
    
cursor = c7.find()
for record in cursor:
    print(record)

cursor = c8.find()
for record in cursor:
    print(record)

cursor = c9.find()
for record in cursor:
    print(record)

cursor = c10.find()
for record in cursor:
    print(record)


