# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:45:05 2017

@author: David Roberts
"""

from googleapiclient import errors
from google_sheets_api import write_row
from serial_read import read_arduino_serial
import time

# Program constants
COLUMNS = ["batch_id", "timestamp", "voltage", "pH", "temperature"]
SPREADSHEET_ID = '1v5JI1Om51v-5gItMuMiNNnmWW8YCQyY8TYk41zsRz8o'
RANGE = 'Automated_Readings!A2:E'
ARDUINO_PORT = "COM4"
BAUD = 9600
WRITE_INTERVAL = 120

# Remember to alter batch_id when running the file on a new batch
BATCH_ID = 1

def main(batch_id):
    """
    Authenticates with Google Sheets API

    In infinite loop, continuously reads serial output from Arduino and writes to google sheets
    """
    
    while True:
        try:
            
            row_dict = read_arduino_serial(ARDUINO_PORT, BAUD)
            row = [batch_id, row_dict['timestamp'], row_dict['voltage'], row_dict['pH'], '']
            write_row(SPREADSHEET_ID, row, RANGE)
            print ("Written Successfully", row)
            time.sleep(WRITE_INTERVAL)
        
        except errors.HttpError as error:

            if error.resp.status in [403, 500, 503]:
                print(error.resp.status)
                time.sleep(5)
             
            else: raise
    
        except Exception:
            
            print("Uncaught Exception \n")
            print(Exception)
            time.sleep(120)
        
if __name__ == "__main__":
    main(BATCH_ID)