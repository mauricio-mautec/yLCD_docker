#!/usr/bin/python 
import Adafruit_DHT
import RPi.GPIO as GPIO
Sensor = Adafruit_DHT.AM2302
pinDHT = 17
pinLED = 4
GPIO.setwarnings(False)
GPIO.setmode (GPIO.BCM)
GPIO.setup   (pinLED, GPIO.OUT)
GPIO.output (pinLED, GPIO.HIGH)
humidity, temp = Adafruit_DHT.read_retry (Sensor, pinDHT)
print (f"Temperture {temp} Humidity {humidity}")
GPIO.output (pinLED, GPIO.LOW)
