# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 16:11:04 2017

@author: David Roberts
"""

import serial
import datetime
import json
import time
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
    
    arduino = serial.Serial(port, baud, timeout = 1)  # open serial port
    arduino.read()
    row_string = arduino.readline()[0:-2].decode('utf-8').replace("'", "\"")
    
    if isinstance(row_string, str) and len(row_string) < 3:
        logger.warning("Arduino Serial passed string under 3 characters, waiting 20 sec for next line\n" +
                       "Row String: " + str(row_string))
        time.sleep(20)
        row_string = arduino.readline()[0:-2].decode('utf-8').replace("'", "\"")
    elif row_string is None:
        logger.warning("Arduino Serial passed None, waiting 20 sec for next line\n" +
                       "Row String: " + str(row_string))
        time.sleep(20)
        row_string = arduino.readline()[0:-2].decode('utf-8').replace("'", "\"")
    
    row_dict = json.loads(row_string)
    row_dict['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    arduino.close()            
    return row_dict