#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
import os

relay = os.getenv("RELAY", 14)

try:
    GPIO.setwarnings(False)

    try:
        GPIO.cleanup()
    except:
        pass

    GPIO.setmode( GPIO.BCM )
    GPIO.setup( relay, GPIO.OUT )
    GPIO.output( relay, GPIO.LOW )
except:
    pass

GPIO.setmode( GPIO.BCM )
GPIO.setup( relay, GPIO.OUT )
GPIO.output( relay, GPIO.LOW )

def openGate():
    GPIO.output( relay, GPIO.HIGH )
    sleep( 1 )
    GPIO.output( relay, GPIO.LOW )
    # print( "door opened" )
