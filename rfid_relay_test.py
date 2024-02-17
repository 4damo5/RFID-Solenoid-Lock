from google.oauth2 import service_account
from Google import Create_Service

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from datetime import datetime
import threading


#relay stuff when u get to it:
#https://www.youtube.com/watch?v=gJZmbqq2-5U&ab_channel=NerdCave

#got google writing source code from this dude:
#https://www.youtube.com/watch?v=YF7Ad-7pvks&ab_channel=JieJenn
#https://www.youtube.com/playlist?list=PL3JVwFmb_BnSee8RFaRPZ3nykuMRlaQp1

#the google sheets bs stuff
CLIENT_SECRET_FILE = 'client_secret.json'

API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION, SCOPES)

spreadsheet_id = "YOUR SPREADSHEET ID" #make sure the spreadsheet is set to writer for anyone who has link
mySpreadsheets = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

#more google sheets bs
worksheet_name = 'Sheet1' #change if the spreadsheet is named somethin different

#ids verified
valid_ids = [] #enter your tag ids

#reading var 
reader = SimpleMFRC522()

#relay stuffs
GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

#start closed
GPIO.output(18,0)

#time var in utc time
curr_time = datetime.now()

def data_send(t,i,tx):
    values = [
    [t,i,tx]
    ]

    #append it as columns
    value_range_body = {
        'values': values
    }

    #do the stuff in the sheet wooo magic
    service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id,
    valueInputOption='USER_ENTERED',
    range=worksheet_name + '!A2:C2',
    body=value_range_body
    ).execute()

#this function basically just checks every 5 seconds if there is a tick checked in the spreadsheet as a failsafe
def read_spread():
    while True:
        response = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        majorDimension='ROWS',
        range='Sheet1!E2:E2'
    ).execute()
        #print(response['values'])
        if response['values'] == [['TRUE']]:

            GPIO.output(18,1)
            time.sleep(5)

            GPIO.output(18,0)
        time.sleep(5)

#runs read_spread on another thread to run simultaneously
reader_thread = threading.Thread(target=read_spread)
reader_thread.daemon = True  # Allows the thread to be killed when the main program exits
reader_thread.start()

#test loop to see if everything works
while True:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    print("Place tag: ")
    try:
        id, text = reader.read()

        #keep track of the time after id is read
        
        #if the id is valid, open lock
        if id in valid_ids:
            GPIO.output(18,1)

        else:
            print('invalid id')

    finally:
    #do the end stuff 
        data_send(curr_time.strftime('%c'), id, text)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
    
    #end closed
    time.sleep(5)
    GPIO.output(18,0)
    time.sleep(2)