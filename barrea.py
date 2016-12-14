#!/usr/bin/env python2.7

import RPi.GPIO as GPIO
import sys
import time
import ibmiotf.device

try:
  options = {
    "org": "7tgk9r",
    "type": "CherrySwitch",
    "id": "cherrySwitch1",
    "auth-method": "token",
    "auth-token": "verywelcome",
    "clean-session": "true"
  }
  client = ibmiotf.device.Client(options)
  client.connect()
except ibmiotf.ConnectionException as e:
  print("ibmiotf ConnectionException")

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, GPIO.PUD_UP)

def publishData(channel):
    try:
        payload = {'state' : GPIO.input(21), 'timestamp': time.time()}
        client.publishEvent("status", "json", payload)
        print(GPIO.input(21))
    except:
        pass

try:
    GPIO.add_event_detect(21, GPIO.BOTH, callback=publishData)

    while(True):
        time.sleep(3600.0)
except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
