#Importing required modules
from pymongo import MongoClient
import time
import RPi.GPIO as GPIO
import time

#Pi3 pins For traffic lights
SDI   = 11
CLK  = 13
LATCH = 15
OE = 12

#Pi3 pins 7-Segment Counter
SDI_C = 29
OE_C = 31
LATCH_C = 33
CLK_C = 35

#binary representation for selecting each digit
digit = [0b10000000, 0b01000000, 0b00100000, 0b00010000]

#binary representation of each number to be displayed on 7-Segmente display
segment = [0b01111110, 0b00000110, 0b01101101, 0b01111001, 0b00110011, 0b01011011, 0b01011111, 0b01110000, 0b01111111, 0b01111011]
#               0           1          2          3            4          5             6            7          8           9

traffic_post_ID = "TP1"

#Setting up the Pi pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)    
GPIO.setup(SDI, GPIO.OUT)
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(LATCH, GPIO.OUT)
GPIO.setup(OE, GPIO.OUT)
GPIO.output(SDI, GPIO.LOW)
GPIO.output(CLK, GPIO.LOW)
GPIO.output(LATCH, GPIO.LOW)
GPIO.output(OE, GPIO.HIGH)
GPIO.output(OE, 1)
GPIO.setup(SDI_C, GPIO.OUT)
GPIO.setup(CLK_C, GPIO.OUT)
GPIO.setup(LATCH_C, GPIO.OUT)
GPIO.setup(OE_C, GPIO.OUT)
GPIO.output(SDI_C, GPIO.LOW)
GPIO.output(CLK_C, GPIO.LOW)
GPIO.output(LATCH_C, GPIO.LOW)
GPIO.output(OE_C, GPIO.HIGH)
GPIO.output(OE_C, 1)

#Connecting to Mongodb database
client = MongoClient('mongodb://root:devashishbittu@cluster0-shard-00-00-kckqv.mongodb.net:27017,cluster0-shard-00-01-kckqv.mongodb.net:27017,cluster0-shard-00-02-kckqv.mongodb.net:27017/TEST?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
db = client.TEST
collection = db['DENSITY']
collection1 = db['TRAFFIC_POST']

#Sending number to timer control circuit for display
def shiftout_1(byte):
    byte = int(byte)
    for w in range (0,10):
        if (byte == w):
            byte = segment[w]
            break
    #Sending the number to the 595 shift register controlling timers
    for x in range(8):
        GPIO.output(SDI_C, (byte >> x) & 1)
        GPIO.output(CLK_C, 1)
        time.sleep(0.00012)
        GPIO.output(CLK_C, 0)

#Output of 595 is turned off
def loading():
    GPIO.output(LATCH_C, 0)
    pass

#Output of 595 is turned on
def latching():
    GPIO.output(LATCH_C, 1)
    GPIO.output(OE_C, 0)
    pass

#Main loop for timer circuit
def display(number):
    
    for w in range (0,3):
        shiftout_1(number % 10)
        number = int(number/10)
    pass

#Sending traffic signal to 595 sfit register controlling traffic lights
def shiftout(byte):
    
    GPIO.output(LATCH, 0)
    for x in range(24):
        GPIO.output(SDI, (byte >> x) & 1)
        GPIO.output(CLK, 1)
        time.sleep(0.001)
        GPIO.output(CLK, 0)
    GPIO.output(LATCH, 1)

GPIO.output(OE, 1)
shiftout(~(0x084210))
GPIO.output(OE, 0)


#Fetching time data for each lane of a post from ATC database
def fetch():
    global Time
    #global EVTM
    Time = []
    result = collection1.find_one({'post_id_PK': traffic_post_ID}, {'_id':0, 'device':1})
    for record in result:
        print(record.['device'])
        lane = record.['device']
    for x in range(len(device)):
        result = collection.find_one({"lane_id_PK" : lane[i]}, {'_id':0, 'time':1})
        for record in result:
            print(record)
            Time.append(record)
        #EVTM=UpdatedDocument['EVTM']
        print("Time: ")
        print (Time)
        #print("EVTM")
        #print(EVTM)
        #emergency()
        control()
    pass

#Main loop for controlling light and timer
def control():
    delay = 0.65
    #For Lane 1
    if (Time[0] != 0):
        print("Green Red Red Red")
        GPIO.output(OE, 1)
        shiftout(~(0xE04210))
        GPIO.output(OE, 0)
        light1=Time[0]-1
        light2=light1+10
        light3=light2+Time[1]+10
        for i in range (0,Time[0]):
                #Checking for emergency vehicle presence
                #emergency()
                loading()
                display(light1-i)
                display(light2-i)
                display(light3-i)
                latching()
                time.sleep(delay)

    #For Lane 1
    if (Time[0] != 0):
        print("Yellow Red Red Red")
        GPIO.output(OE, 1)
        shiftout(~(0x104210))
        GPIO.output(OE, 0)
        light1=10-1
        light2=light2-Time[0]
        light3=light3-Time[0]
        for i in range (0,10):
                #Checking for emergency vehicle presence
                #emergency()
                loading()
                display(light1-i)
                display(light2-i)
                display(light3-i)
                latching()
                time.sleep(delay)

    #For lane 2
    if (Time[1] != 0):
        print("Red Green Red Red")
        GPIO.output(OE, 1)
        shiftout(~(0x0F0210))
        GPIO.output(OE, 0)
        light1=Time[1]+10+Time[2]+10
        light2=Time[1]-1
        light3=light3-10
        for i in range (0,Time[1]):
                #Checking for emergency vehicle presence
                #emergency()
                loading()
                display(light1-i)
                display(light2-i)
                display(light3-i)
                latching()
                time.sleep(delay)

    #For Lane 2
    if (Time[1] != 0):
        print("Red Yellow Red Red")
        GPIO.output(OE, 1)
        shiftout(~(0x088210))
        GPIO.output(OE, 0)
        light1=light1-Time[1]
        light2=10-1
        light3=light3-Time[1]
        for i in range (0,10):
                #Checking for emergency vehicle presence
                #emergency()
                loading()
                display(light1-i)
                display(light2-i)
                display(light3-i)
                latching()
                time.sleep(delay)

    #For Lane 3
    if (Time[2] != 0):
        print("Red Red Green Red")
        GPIO.output(OE, 1)
        shiftout(~(0x087810))
        GPIO.output(OE, 0)
        light1=light1-10
        light2=Time[2]+10Time[0]+10
        light3=Time[2]-1
        for i in range (0,Time[2]):
                #Checking for emergency vehicle presence
                #emergency()
                #print(i+1)
                loading()
                display(light1-i)
                display(light2-i)
                display(light3-i)
                latching()
                time.sleep(delay)

    #For Lane 3
    if (Time[2] != 0):
        print("Red Red Yellow Red")
        GPIO.output(OE, 1)
        shiftout(~(0x084410))
        GPIO.output(OE, 0)
        light1=light1-Time[2]
        light2=light2-Time[2]
        light3=10-1
        for i in range (0,10):
                #Checking for emergency vehicle presence
                #emergency()
                loading()
                display(light1-i)
                display(light2-i)
                display(light3-i)
                latching()
                time.sleep(delay)

    #For Lane 4      
    if (Time[3] != 0):
        print("Red Red Red Green")
        GPIO.output(OE, 1)
        shiftout(~(0x0843C0))
        GPIO.output(OE, 0)
        x=Time[3]
        for i in range (0,Time[3]):
                #Checking for emergency vehicle presence
               # emergency()
                loading()
                display(x-i)
                display(x-i)
                display(x-i)
                latching()
                time.sleep(delay)

    #For Lane 4
    if (Time[3] != 0):
        print("Red Red Red Yellow")
        GPIO.output(OE, 1)
        shiftout(~(0x084220))
        GPIO.output(OE, 0)
        x=10
        for i in range (0,10):
                #Checking for emergency vehicle presence
                #emergency()
                loading()
                display(x-i)
                display(x-i)
                display(x-i)
                latching()
                time.sleep(delay)
                
    pass

#Main loop to check presence of emergency vehicle in a Lane
# def emergency():
#     global EVTM
#     #Fetching data from ATC data acquired from EVTM
#     UpdatedDocument = collection.find_one({"ID" : 1})
#     EVTM=UpdatedDocument['EVTM']
#     #If vehicle in Lane 1 turn it Green
#     if (EVTM[0] == "Emergency"):
#         print("Green Red Red Red")
#         GPIO.output(OE, 1)
#         shiftout(~(0xE04210))
#         GPIO.output(OE, 0)
#         while (EVTM[0] == "Emergency"):
#             UpdatedDocument = collection.find_one({"ID" : 1})
#             EVTM=UpdatedDocument['EVTM']
#         print("Emergency Solved")
#         fetch()
#     #If vehicle in Lane 2 turn it Green        
#     elif (EVTM[1] == "Emergency"):
#         print("Red Green Red Red")
#         GPIO.output(OE, 1)
#         shiftout(~(0x0F0210))
#         GPIO.output(OE, 0)
#         while (EVTM[1] == "Emergency"):
#             UpdatedDocument = collection.find_one({"ID" : 1})
#             EVTM=UpdatedDocument['EVTM']
#         print("Emergency Solved")
#         fetch()
#     #If vehicle in Lane 3 turn it Green
#     elif (EVTM[2] == "Emergency"):
#         print("Red Red Green Red")
#         GPIO.output(OE, 1)
#         shiftout(~(0x087810))
#         GPIO.output(OE, 0)
#         while (EVTM[2] == "Emergency"):
#             UpdatedDocument = collection.find_one({"ID" : 1})
#             EVTM=UpdatedDocument['EVTM']
#         print("Emergency Solved")
#         fetch()
#     #If vehicle in Lane 4 turn it Green
#     elif (EVTM[3] == "Emergency"):
#         print("Red Red Red Green")
#         GPIO.output(OE, 1)
#         shiftout(~(0x0843C0))
#         GPIO.output(OE, 0)
#         while (EVTM[3] == "Emergency"):
#             UpdatedDocument = collection.find_one({"ID" : 1})
#             EVTM=UpdatedDocument['EVTM']
#         print("Emergency Solved")
#         fetch()
    
#     pass


#Infinity loop for real time control
while(1):
    try:
        print ("Starting!")
        fetch()
        print("Fetched")
    #Debugging any error if occurred
    except:
        print ("Error Occured!")
        pass



