#!/usr/bin/env python

from time import sleep
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

import RPi.GPIO as GPIO
import datetime
import httplib
import urllib

GPIO.setmode(GPIO.BCM)  # Set's GPIO pins to BCM GPIO numbering
INPUT_PIN = 4           # Sets our input pin, in this example I'm connecting our button to pin 4. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
GPIO.setup(INPUT_PIN, GPIO.IN)  # Set our input pin to be an input

mail_from = 'deurbel@gmail.com'
mail_to = ['susan.krieger@gmail.com','marius.hettema@gmail.com']
mail_subject = '*** LIEFJE, de DEURBEL gaat'
mail_smtp = 'smtp.xs4all.nl'

pushover_apptoken = "TOKEN"
pushover_userkey = "u7x96iy34coy4dnvi4qnye8yb6voog"

# Create a function to run when the input is high
def deurbel(channel):
    now = datetime.datetime.now();
    print now.strftime("%Y-%m-%d %H:%M:%S deurbel")
    mail()
    #pushover_alert()

# read raw input
def readInput():
    if (GPIO.input(INPUT_PIN) == True): # Physically read the pin now
        print('3.3')
    else:
        print('0')

def mail():
    try:
        msg = MIMEText('', 'plain') #empty body
        msg['Subject']= mail_subject
        msg['From']   = mail_from

        conn = SMTP(mail_smtp)
        conn.set_debuglevel(False)
        try:
            conn.sendmail(mail_from, mail_to, msg.as_string())
        finally:
            conn.quit()

    except Exception, exc:
        print "mail failed; %s" % str(exc) 

def pushover_alert():
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.urlencode({
        "token": pushover_apptoken,
        "user": pushover_userkey,
        "message": mail_subject,
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

# add callback to deurbel method when input goes to low
GPIO.add_event_detect(INPUT_PIN, GPIO.FALLING, callback=deurbel, bouncetime=250)

print "start listening..."

# Start a loop that never ends
while True:
    #readInput();
    sleep(1);           # Sleep for a full second before restarting our loop

print "finished"
