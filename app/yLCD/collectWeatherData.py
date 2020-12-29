#!/usr/bin/python
import sys
from dsp.weather.collect import WeatherCollector

def saveWeather (source, codigo):
    weather     = WeatherCollector (source)
    clima       = weather.getWeather (codigo)
    if clima: weather.saveWeather()

if len(sys.argv) != 2:
    print ("Usage: ./collectWeather.py <source> ")
    exit()

#saveWeather (sys.argv[1], 'Santa Maria da Feira, PT')
saveWeather (sys.argv[1], 'GYN') 
saveWeather (sys.argv[1], 'CLV') 
saveWeather (sys.argv[1], 'APA')
