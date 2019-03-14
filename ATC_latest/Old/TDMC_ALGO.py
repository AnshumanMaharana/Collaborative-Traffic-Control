from pymongo import MongoClient
import time


#conn  = MongoClient('mongodb://root:devashishbittu@cluster0-shard-00-00-kckqv.mongodb.net:27017,cluster0-shard-00-01-kckqv.mongodb.net:27017,cluster0-shard-00-02-kckqv.mongodb.net:27017/TDMC?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
#db = conn.TDMC
status = True
while (status):
	try:
		print("Connecting......")
		conn  = MongoClient('mongodb+srv://root:devashishbittu@cluster0-kckqv.mongodb.net/TEST?retryWrites=true&ssl=true&ssl_cert_reqs=CERT_NONE')
		print("Connected successfully!!!")
		db = conn.TEST
		traffic_post_collection = db.TRAFFIC_POST
		density_collection = db.DENSITY
		status = False
	except Exception as e:
		print(e)
		print("Could not connect to MongoDB. Trying again!")
		time.sleep(10)

#Time required for a traffic post cycle
fixed_time=2*60.00
threshold = 0


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
	time_update(time,lane)

def time_update(time,lane):
	for i in range(len(time)):
		result = density_collection.update_one({"density_id_PK" : lane[i]}, {"$set" : {"time" : time[i]}})


if __name__ == '__main__':
	while(1):
		try:
			print("Starting!")
			start_time = time.time()
			lane = fetch_density()
			print("Execution time: ", time.time() - start_time, " sec")
			for i in range(len(lane)):
				result = density_collection.find({'density_id_PK': lane[i]} , {'_id':0 , 'time':1})
				for record in result:
					print("Lane "+ str(i+1)+ ": " + str(record['time']))
		except Exception as e:
			print(e)
			print("Error Occured!")
			print("Connecting Again!")


