import time
import RPi.GPIO as GPIO
import os
import random
import logging

logging.basicConfig(filename='/home/pi/atc-module/atc.log')


#Pi3 pins For traffic lights
SDI   = 11
CLK  = 13
LATCH = 15
OE = 12

Green_Time = []
Default_Green_Time = []
Yellow_Time = 5
Signal = []
Green_Signal_Byte = []
Yellow_Signal_Byte = []

No_of_lanes = 4

ON_Byte = ""

def config_pi():
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


def shiftout(byte):
    GPIO.output(LATCH, 0)
    for x in range(4*No_of_lanes):
        GPIO.output(SDI, (byte >> x) & 1)
        GPIO.output(CLK, 1)
        time.sleep(0.001)
        GPIO.output(CLK, 0)
    GPIO.output(LATCH, 1)

def intialize_lights():
        logging.warning("ON")
        GPIO.output(OE, 1)
        temp_on = list(ON_Byte)
        On_Byte = "".join(temp_on)
        hex_int = int(On_Byte, 16)
        logging.warning("Byte:",hex(hex_int))
        shiftout(~(hex_int))#0b11111111
        GPIO.output(OE, 0)
        time.sleep(3)
        logging.warning("OFF")
        GPIO.output(OE, 1)
        shiftout((hex_int))#0b11111111
        GPIO.output(OE, 0)
        time.sleep(3)
        logging.warning("Done")

def byte_def():

    global ON_Byte
    global Default_Green_Time
    Default_Green_Time = []
    logging.warning("Generating!")
    Byte = "0x"
    ON_Byte = "0x"
    for i in range(No_of_lanes):
        Default_Green_Time.append(5)
        Signal.append("Red")
        Byte = Byte + "1"
        ON_Byte = ON_Byte + "F"

    for i in range(No_of_lanes):
        temp_g = list(Byte)
        temp_y = list(Byte)
        temp_g[i+2] = "C"
        temp_y[i+2] = "2"
        Green_Byte = "".join(temp_g)
        Yellow_Byte= "".join(temp_y)
        hex_int = int(Green_Byte, 16)
        Green_Signal_Byte.append(hex_int)
        logging.warning("Byte:",hex(hex_int))
        hex_int = int(Yellow_Byte, 16)
        Yellow_Signal_Byte.append(hex_int)
        logging.warning("Byte:",hex(hex_int))

    logging.warning("Green Time: "+str(Green_Time))
    logging.warning("Green_Signal_Byte: "+str(Green_Signal_Byte))
    logging.warning("Yellow_Signal_Byte: "+str(Yellow_Signal_Byte))
    logging.warning("Generated!")

def initialize_timing(Green_Time):

    global Red_Time
    Red_Time = []
    for i in range (0,len(Green_Time)):
    	if Green_Time[i] != 0:
                Red_Time.append( ((len(Green_Time)-1)*Yellow_Time) + sum(Green_Time) - Green_Time[i] )
    	else:
    		Red_Time.append(0)
    logging.warning("Red Time: "+str(Red_Time))

def data_fetch(data_status=True):
    while(data_status):
        data = ""
        try:
            file = open("data.txt","r")
            for line in file:
                data = line
            file.close()
            data_status = False
            return data

        except Exception as e:
            logging.warning(e)
            data_status = True

def delay_one_second(second,byte):
    timeout = time.time() + second
    while True:
        shiftout(~byte)
        if time.time() > timeout:
            break

def lights_control():
        logging.warning("\nStarting controller!")
        for lane in range(len(Green_Time)):
            if Green_Time[lane] == 0:
                logging.warning("\nDoes not exist!")
            else:
                Signal[lane] = "Green"
                logging.warning("Signal: "+str(Signal))
                logging.warning("Red Time: "+str(Red_Time))
                GPIO.output(OE, 1)
                shiftout(~Green_Signal_Byte[lane])
                GPIO.output(OE, 0)
                for i in range(Green_Time[lane]):
                    for j in range(len(Red_Time)):
                        shiftout(~Green_Signal_Byte[lane])
                        if (j != lane) and (Red_Time[j] != 0):
                            Red_Time[j] -= 1
                    #time.sleep(1)
                    delay_one_second(1,Green_Signal_Byte[lane])
                logging.warning("Red Time: "+str(Red_Time))
                Signal[lane] = "Yellow"
                logging.warning("Signal: "+str(Signal))
                GPIO.output(OE, 1)
                shiftout(~Yellow_Signal_Byte[lane])
                GPIO.output(OE, 0)
                for i in range(Yellow_Time):
                    for j in range(len(Red_Time)):
                        shiftout(~Yellow_Signal_Byte[lane])
                        if (j != lane) and (Red_Time[j] != 0):
                             Red_Time[j] -= 1
                    #time.sleep(1)
                    delay_one_second(1,Yellow_Signal_Byte[lane])
                logging.warning("Red Time: "+str(Red_Time))
                Signal[lane] = "Red"

if __name__ == '__main__':
    config_pi()
    byte_def()
    intialize_lights()
    while(1):
        text = data_fetch()
        if(text == ""):
            logging.warning("Data not found!")
            continue
        elif(text == "Error"):
            logging.warning("Error in file!")
            Green_Time = []
            Green_Time = Default_Green_Time
            logging.warning("Green Time: "+str(Green_Time))
        else:
            data = ""
            Green_Time = []
            temp = list(text)
            for i in range(1,len(temp)):
                if ((temp[i] == ',') or (temp[i] == ']')):
                    Green_Time.append(int(data))
                    data = ""
                    continue
                data = data + temp[i]
            logging.warning("Green Time: "+str(Green_Time))
        initialize_timing(Green_Time)
        lights_control()


