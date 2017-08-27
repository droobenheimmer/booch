# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:45:05 2017

@author: David Roberts
"""

import time
import os
import subprocess
import argparse
import cgitb
import logging

from googleapiclient import errors
from google_sheets_api import write_row
from serial_read import read_arduino_serial

logging.basicConfig(filename='pH_readings.log',level=logging.DEBUG)
logger = logging.getLogger(__name__)

cgitb.enable(format='text')

# Parse batch number
parser = argparse.ArgumentParser(description='Retrieve arguments')
parser.add_argument('--batch', nargs='?', const=1, type=int)
args = parser.parse_args()

# Establish program constants
COLUMNS = ["batch_id", "timestamp", "voltage", "pH", "temperature"]

BATCH_ID = 3
PORT_NAME = os.environ.get("PORT_NAME")
ARDUINO_EXE = os.environ.get("ARDUINO_EXE")
SPREADSHEET_ID = os.environ.get("GOOGLE_SPREADSHEET_ID")
PROJECT_FILE = "./ph_meter/ph_meter.ino"
RANGE = 'Automated_Readings!A2:E'
BAUD = 9600
WRITE_INTERVAL = 120


# Remember to alter batch_id when running the file on a new batch
def main(batch_id):
    """
    Authenticates with Google Sheets API

    In infinite loop, continuously reads serial output from Arduino and writes to google sheets
    """
           
    pH_meter_process = upload_arduino_script(ARDUINO_EXE, PORT_NAME, PROJECT_FILE)

    while True:

        # poll process to ensure that it's still running, if not None, reupload arduino script
        if pH_meter_process.poll():
            pH_meter_process = upload_arduino_script(ARDUINO_EXE, PORT_NAME, PROJECT_FILE)
	
        try:
            
            row_dict = read_arduino_serial(PORT_NAME, BAUD)
            row = [batch_id, row_dict['timestamp'], row_dict['voltage'], row_dict['pH'], '']
            write_row(SPREADSHEET_ID, row, RANGE)
            logger.info("Written Successfully: " + str(row))
            time.sleep(WRITE_INTERVAL)
        
        except errors.HttpError as error:

            if error.resp.status in [403, 500, 502, 503]:
                print(error.resp.status)
                time.sleep(5)
             
            else: raise
    
        except Exception as e:
            logger.exception("Uncaught Exception")
            time.sleep(WRITE_INTERVAL)
            
def upload_arduino_script(arduino_exe, port, project_file):
    """
    Builds arduino command string from provided parameters
    
    Runs subprocess to compile and upload arduino code
    """
    
    arduino_command =  arduino_exe  + " --upload " + "--port " + port + " " + project_file
                       
    print ("\n\n-- Arduino Command --")
    print (arduino_command)
    
    print ("-- Starting Upload --\n")
    
    p = subprocess.Popen(arduino_command, shell=True, stdin=None, stdout=None, stderr=None)

    time.sleep(5)
    
    return p
        
if __name__ == "__main__":
    
    main(BATCH_ID)