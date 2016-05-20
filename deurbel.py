#!/usr/bin/env python

from time import sleep
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

import RPi.GPIO as GPIO
import datetime

GPIO.setmode(GPIO.BCM)  # Set's GPIO pins to BCM GPIO numbering
INPUT_PIN = 4           # Sets our input pin, in this example I'm connecting our button to pin 4. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
GPIO.setup(INPUT_PIN, GPIO.IN)  # Set our input pin to be an input

# Create a function to run when the input is high
def deurbel(channel):
    now = datetime.datetime.now();
    print now.strftime("%Y-%m-%d %H:%M:%S deurbel!")
    mail()

# read raw input
def readInput():
    if (GPIO.input(INPUT_PIN) == True): # Physically read the pin now
        print('3.3')
    else:
        print('0')

def mail():
    try:
        msg = MIMEText('deurbel', 'plain')
        msg['Subject']= '*** LIEFJE, de DEURBEL gaat'
        msg['From']   = 'deurbel@gmail.com'

        conn = SMTP('smtp.xs4all.nl')
        conn.set_debuglevel(False)
        try:
            conn.sendmail('deurbel@gmail.com', 'susan.krieger@gmail.com', msg.as_string())
        finally:
            conn.quit()

    except Exception, exc:
        print "mail failed; %s" % str(exc) 

# add callback to deurbel method when input goes to low
GPIO.add_event_detect(INPUT_PIN, GPIO.FALLING, callback=deurbel, bouncetime=200)

print "start listening..."

# Start a loop that never ends
while True:
    #readInput();
    sleep(1);           # Sleep for a full second before restarting our loop

print "finished"
