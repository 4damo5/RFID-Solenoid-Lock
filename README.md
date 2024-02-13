 #RFID-Solenoid-Lock

First of all, the Google.py is not made by me but it makes the spreadsheet integration easier (it's by [Jie Jenn](https://www.youtube.com/@jiejenn))
Basically this runs (for me) on my RPi 3 and it just uses a RC522 to read an RFID card. If the card is on the validation list, it will open the lock, and send that data over to the Google Spreadsheet assigned to it.
The timestamps are based on runtime so they might look funny and could be changed to real time values. 
Sadly, I burnt out the solenoid lock so I gotta get a new one but I know the code works (YOUR LOCK WONT BURN OUT I JUST LEFT THE SOLENOID ACTIVE IN TESTING)
Anyways, it works.
