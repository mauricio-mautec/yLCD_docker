#!/usr/bin/python
import sqlite3
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import configparser
from   pathlib import Path

Sensor = Adafruit_DHT.AM2302
pinDHT = 17
pinLED = 4

GPIO.setwarnings(False)
GPIO.setmode (GPIO.BCM)
GPIO.setup   (pinLED, GPIO.OUT)

def getDatabaseName():
    here          = Path(__file__).parent / 'dsp/weather/weather.ini'
    config        = configparser.ConfigParser()
    config.read   (here)
    return config['database']['weather']

def setNewCollectData (source, location):
    conn    = sqlite3.connect (getDatabaseName())
    curs    = conn.cursor()
    stmt    = """INSERT INTO collectDataSource VALUES (datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))"""
    curs.execute (stmt, (source, location));
    conn.commit()
    return curs.lastrowid


#    stmt    = "select rowid from collectData WHERE SOURCE = (?) AND LOCATION = (?) ORDER BY ROWID DESC LIMIT 1"
#    curs    = conn.cursor()
#    curs.execute (stmt, (source, location));
#    collectData = curs.fetchone()
#    conn.commit()
#    conn.close()
#    return collectData[0]


def saveWeather ():
    GPIO.output (pinLED, GPIO.HIGH)
    collectData    = setNewCollectData('RBPI Weather Station', 'Home GYN')
    humidity, temp = Adafruit_DHT.read_retry (Sensor, pinDHT)

    if humidity is not None and temp is not None and humidity != 0 and temp < 100 and humidity <= 100:
        datavar = [ (collectData, 'humidity',        'percent', humidity ),
                    (collectData, 'temperature',     'celsius', temp     )]
        
        conn    = sqlite3.connect (getDatabaseName())
        curs    = conn.cursor()
        stmt    = """INSERT INTO collectData VALUES (?,?,?,?)"""
        curs.executemany (stmt, datavar)
        conn.commit()
        conn.close()
    
    GPIO.output (pinLED, GPIO.LOW)
        
saveWeather()
