# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:45:05 2017

@author: David Roberts
"""

import time
import os
import subprocess
import argparse

from googleapiclient import errors
from google_sheets_api import write_row
from serial_read import read_arduino_serial

# Parse batch number
#parser = argparse.ArgumentParser(description='Retrieve arguments')
#parser.add_argument('--batch', nargs='?', const=1, type=int)
#args = parser.parse_args()

# Establish program constants
COLUMNS = ["batch_id", "timestamp", "voltage", "pH", "temperature"]

BATCH_ID = 2
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
    try:        
        
        upload_arduino_script(ARDUINO_EXE, PORT_NAME, PROJECT_FILE)
    
    except Exception:
        
        print("Failed to upload Arduino code")
        return 0
    
    while True:
        try:
            
            row_dict = read_arduino_serial(PORT_NAME, BAUD)
            row = [batch_id, row_dict['timestamp'], row_dict['voltage'], row_dict['pH'], '']
            write_row(SPREADSHEET_ID, row, RANGE)
            print ("Written Successfully", row)
            time.sleep(WRITE_INTERVAL)
        
        except errors.HttpError as error:

            if error.resp.status in [403, 500, 502, 503]:
                print(error.resp.status)
                time.sleep(5)
             
            else: raise
    
        except Exception:
            
            print("Uncaught Exception \n")
            print(Exception.with_traceback)
            time.sleep(WRITE_INTERVAL)
            
def upload_arduino_script(arduino_exe, port, project_file):
    """
    Builds arduino command string from provided parameters
    
    Runs subprocess to compile and upload arduino code
    """
    
    arduino_command =  arduino_exe  + " --upload " + "--port " + port + " " + project_file
                       
    print ("\n\n -- Arduino Command --")
    print (arduino_command)
    
    print ("-- Starting Upload --\n")
    
    presult = subprocess.call(arduino_command, shell=True)
    
    if presult != 0:
        print ("\n Failed - result code = {}".format(presult))
    else:
        print ("\n-- Success --")
        
if __name__ == "__main__":
    
    main(BATCH_ID)