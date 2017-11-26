# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 16:11:04 2017

@author: David Roberts
"""

import serial
import datetime
import json
import time
import os
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

def read_arduino_serial(port, baud):
    """
    Opens a connection to arduino serial port
    Reads initial byte and a line
    Generates dictionary from line
    Closes connection 
    Returns dict
    """
    
    arduino = serial.Serial(port, baud, timeout = 15)  # open serial port
    row_string = take_last_observation(arduino)
    
    if isinstance(row_string, str) and len(row_string) < 3:
        logger.warning("Arduino Serial passed string under 3 characters, waiting 20 sec for next line\n" +
                       "Row String: " + str(row_string))
        time.sleep(20)
        row_string = take_last_observation(arduino)
    elif row_string is None:
        logger.warning("Arduino Serial passed None, waiting 20 sec for next line\n" +
                       "Row String: " + str(row_string))
        time.sleep(20)
        row_string = take_last_observation(arduino)
    
    print("Loading Following String to Json:", row_string)
    row_dict = json.loads(row_string)
    row_dict['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    arduino.close()            
    return row_dict

def take_last_observation(arduino_serial):
    """
    Takes an Serial object
    Reads the last line, partitions on open bracket
    Returns string
    """
    
    line = arduino_serial.readline()
    print("Read serial line: ", line)
    row_string = line.decode('utf-8').replace("'", "\"")
    
    if '}' in row_string:
        return "{" + row_string.rpartition("{")[-1]
    else:
        return ""

if __name__ == "__main__":
    print(os.environ.get("PORT_NAME"))
    print(read_arduino_serial(os.environ.get("PORT_NAME"), 9600))

        