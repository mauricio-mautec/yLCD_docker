import time
import datetime
import socket
from   dsp.weather.dto import weatherDB
from   dsp.weather.location import *
from   functools import reduce
import logging
import json
from   utility import * 

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Weather:
    def getData (self, info, codigo = 'GYN'):
        self.codigo = codigo
        front_dsp = "info_" + str(info)
        front_exe = getattr(self, front_dsp, self.info_main)
        return front_exe()

#    name  = 'varname'
#    value = 'something'
#    setattr(self, name, value) #equivalent to: self.varname= 'something'

    # Convert Degrees to Direction
    def degToCompass(self,num):
        val=int((num/22.5)+.5)
        arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
        return arr[(val % 16)]


    def info_weather(self):
        horario = time.strftime ("%H:%M")
        calMes  = time.strftime ("%b")
        calWek  = time.strftime ("%a");
        calDay  = time.strftime ("%d");

        # Inside Home Weather Info
        wdb     = weatherDB ({})
        wdb.getCollectData ('Home CLV', 'RBPI Weather Station')
        tempInt = wdb.getMeasure('temperature')
        humInt  = wdb.getMeasure('humidity')

        # Weather Info 
        tempExtList = []
        humExtList  = []
        weatherDesc = []

        wdb.getCollectData ('CLV', 'darksky.net')
        tempExtList.append(wdb.getMeasure('temperature'))
        humExtList.append(wdb.getMeasure('humidity'))
        if wdb.getMeasure('weatherMain') != 0:
            weatherDesc.append(wdb.getMeasure('weatherMain'))

        wdb.getCollectData ('CLV', 'openweathermap.org')
        tempExtList.append( wdb.getMeasure('temperature'))
        humExtList.append( wdb.getMeasure('humidity'))
        if wdb.getMeasure('weatherDesc') != 0:
            weatherDesc.append(wdb.getMeasure('weatherDesc'))

        wdb.getCollectData ('CLV', 'yr.no')
        tempExtList.append( wdb.getMeasure('temperature'))
        humExtList.append( wdb.getMeasure('humidity'))
        if wdb.getMeasure('weatherMain') != 0:
            weatherDesc.append(wdb.getMeasure('weatherMain'))

        humExt  = reduce(lambda x,y: x+y, humExtList) / 3.0
        tempExt = reduce(lambda x,y: x+y, tempExtList) / 3.0
        moon    = "cheia"

        dataWeather =  {
                        "time"        : horario,
                        "mes"         : calMes,
                        "dia"         : calDay,
                        "sem"         : calWek,
                        "temp"        : tempInt,
                        "hum"         : humInt,
                        "tempExt"     : tempExt,
                        "humExt"      : humExt,
                        "description" : weatherDesc,
                        "moon"        : moon }

        return json.dumps(dataWeather)

    def info_main(self):
        # Calendar & Host info
        horario = time.strftime ("%H:%M")
        calMes  = time.strftime ("%b")
        calWek  = time.strftime ("%a");
        calDay  = time.strftime ("%d");

        hostName = socket.gethostname()
        hostIP   = socket.gethostbyname ("Info")

        # Inside Home Weather Info
        wdb     = weatherDB ({})
        wdb.getCollectData ('Home CLV', 'RBPI Weather Station')
        tempInt = wdb.getMeasure('temperature')
        humInt  = wdb.getMeasure('humidity')

        dataWeather = {"tempInt" : tempInt, "humInt" : humInt, "time" : horario, "mes" : calMes, "dia" : calDay, "sem" : calWek }
        return json.dumps(dataWeather)

    def info_cidade(self):
        cidade = self.codigo

        # Calendar & Host info
        horario = time.strftime ("%H:%M")
        calMes  = time.strftime ("%b")
        calWek  = time.strftime ("%a");
        calDay  = time.strftime ("%d");

        hostName = socket.gethostname()
        hostIP   = socket.gethostbyname ("Info")

        # Weather Info 
        wdb     = weatherDB ({})
        wdb.getCollectData (cidade, 'openweathermap.org')
        tempExt             = wdb.getMeasure('temperature')
        temp_max            = int(wdb.getMeasure('temperatureMax')) 
        temp_min            = int(wdb.getMeasure('temperatureMin'))
        sunRise             = datetime.datetime.fromtimestamp(wdb.getMeasure('sunrise'))
        sunrise             = '{}'.format (sunRise.strftime("%H:%M"))
        sunSet              = datetime.datetime.fromtimestamp(wdb.getMeasure('sunset'))
        sunset              = '{}'.format (sunSet.strftime("%H:%M"))
       
        wdb.getCollectData (cidade, 'darksky.net')
        humExt              = wdb.getMeasure('humidity')
        pressure            = wdb.getMeasure('pressure') 
        precipProbability   = wdb.getMeasure('rainProbability')
        dewPoint            = wdb.getMeasure('temperatureDew')
        aparentTemperature  = wdb.getMeasure('temperatureApparent')
        weather             = wdb.getMeasure('weatherMain')
        weather_desc        = wdb.getMeasure('weatherDesc')
        uvIndex             = wdb.getMeasure('skyUVIndex')
        ozone               = wdb.getMeasure('skyOzone')
        visibility          = "%.0f" % wdb.getMeasure('skyVisibility')
        wind_deg            = wdb.getMeasure('windDegrees')
        direction           = self.degToCompass(wind_deg)
        wind_speed          = wdb.getMeasure('windSpeed')

        dataWeather = { "cidade" : cidade, "tempMin" : temp_min, "tempExt" : tempExt, "tempMax" : temp_max, "weather" : weather, "codigo" : self.codigo, "time" : horario, "mes" : calMes, "dia" : calDay, "sem" : calWek, "pressure" : pressure, "humExt" : humExt, "windSpeed" : wind_speed, "precipProbability" : precipProbability, "dewPoint" : dewPoint, "direction" : direction, "uvIndex" : uvIndex, "ozone" : ozone, "visibility" : visibility, "aparent" : aparentTemperature, "sunrise" : sunrise, "sunset" : sunset}
        return json.dumps(dataWeather)
