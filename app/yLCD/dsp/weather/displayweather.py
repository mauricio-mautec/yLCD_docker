import time
import datetime
import socket
from   dsp.weather.dto import weatherDB
from   dsp.weather.location import *
from   flask import request, render_template
import inspect
from   functools import reduce
import logging
from   utility import * 

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DisplayWeather:
    # DISPATCH RENDER FRONT END
    # CREATE NEW DISPLAY USING def display_<name>(self):
    # RENDER TEMPLATE NAMED display_<name>.html
    def renderDisplay (self, display, codigo = 'GYN'):
        self.codigo = codigo
        front_dsp = "display_" + str(display)
        front_exe = getattr(self, front_dsp, self.display_main)
        return front_exe()

#    name  = 'varname'
#    value = 'something'
#    setattr(self, name, value) #equivalent to: self.varname= 'something'

    # Convert Degrees to Direction
    def degToCompass(self,num):
        val=int((num/22.5)+.5)
        arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
        return arr[(val % 16)]

    def getImgWeather(self, weatherDesc):
        listOfImages = ['ChuvaForte','ChuvaTrovao','Lua','Neve','Nublado',' SolNublado','Sol','Vento']
        resultImages = []

        for desc in weatherDesc:
            desc.lower()
            if desc.find("thunderstorm") != -1:
                resultImages.append('ChuvaTrovao')
            elif desc.find("rain") != -1: 
                resultImages.append('ChuvaForte')
            elif desc.find("clear") != -1:
                hora = int(time.strftime("%H"))
                if hora < 19:
                    resultImages.append('Sol')
                else:
                    resultImages.append('Lua')
            elif (desc.find("few clouds") != -1 or  desc.find("scattered clouds") != -1 or  desc.find("few clouds") != -1):
                hora = int(time.strftime("%H"))
                if hora < 19:
                    resultImages.append('SolNublado')
                else:
                    resultImages.append('Lua')
                    resultImages.append('Nublado')
            elif desc.find("overcast clouds") != -1 or desc.find("broken clouds") != -1:
                resultImages.append('Nublado')
        
        return resultImages


    def display_weather(self):
        horario = time.strftime ("%H:%M")
        calMes  = time.strftime ("%b")
        calWek  = time.strftime ("%a");
        calDay  = time.strftime ("%d");

        # Inside Home Weather Info
        wdb     = weatherDB ({})
        wdb.getCollectData ('Home GYN', 'RBPI Weather Station')
        tempInt = wdb.getMeasure('temperature')
        humInt  = wdb.getMeasure('humidity')

        # Weather Info 
        tempExtList = []
        humExtList  = []
        weatherDesc = []

        wdb.getCollectData ('GYN', 'darksky.net')
        tempExtList.append(wdb.getMeasure('temperature'))
        humExtList.append(wdb.getMeasure('humidity'))
        if wdb.getMeasure('weatherMain') != 0:
            weatherDesc.append(wdb.getMeasure('weatherMain'))

        wdb.getCollectData ('GYN', 'openweathermap.org')
        tempExtList.append( wdb.getMeasure('temperature'))
        humExtList.append( wdb.getMeasure('humidity'))
        if wdb.getMeasure('weatherDesc') != 0:
            weatherDesc.append(wdb.getMeasure('weatherDesc'))

        wdb.getCollectData ('GYN', 'yr.no')
        tempExtList.append( wdb.getMeasure('temperature'))
        humExtList.append( wdb.getMeasure('humidity'))
        if wdb.getMeasure('weatherMain') != 0:
            weatherDesc.append(wdb.getMeasure('weatherMain'))

        weatherImgList = self.getImgWeather(weatherDesc)
        humExt  = reduce(lambda x,y: x+y, humExtList) / 3.0
        tempExt = reduce(lambda x,y: x+y, tempExtList) / 3.0
        moon    = "cheia"

        template = 'weather/' + inspect.currentframe().f_code.co_name + ".html"
        return render_template(template, 
                                time = horario, mes = calMes, dia = calDay,
                                sem = calWek, temp = tempInt, hum = humInt,
                                tempApa = tempExt, humApa = humExt,
                                images = weatherImgList, moon = moon)

    # DEFAULT FRONT END DISPLAY
    # TEMPLATE display_main.html 
    def display_main(self):
        # Calendar & Host info
        horario = time.strftime ("%H:%M")
        calMes  = time.strftime ("%b")
        calWek  = time.strftime ("%a");
        calDay  = time.strftime ("%d");

        hostName = socket.gethostname()
        hostIP   = socket.gethostbyname ("rbpidisplay")

        # Inside Home Weather Info
        wdb     = weatherDB ({})
        wdb.getCollectData ('Home GYN', 'RBPI Weather Station')
        tempInt = wdb.getMeasure('temperature')
        humInt  = wdb.getMeasure('humidity')

        template = 'weather/' + inspect.currentframe().f_code.co_name + ".html"
        return render_template (template, tempInt = tempInt, humInt = humInt, 
                                time = horario, mes = calMes, dia = calDay, sem = calWek )

    def display_cidade(self):
        cidade = self.codigo

        # Calendar & Host info
        horario = time.strftime ("%H:%M")
        calMes  = time.strftime ("%b")
        calWek  = time.strftime ("%a");
        calDay  = time.strftime ("%d");

        hostName = socket.gethostname()
        hostIP   = socket.gethostbyname ("rbpidisplay")

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

        template = 'weather/' + inspect.currentframe().f_code.co_name + ".html"
        return render_template (template, cidade = cidade, tempMin = temp_min, tempExt = tempExt,
                tempMax   = temp_max, weather = weather, codigo = self.codigo,
                time      = horario,      mes = calMes, dia = calDay, sem = calWek,
                pressure          = pressure,           humExt   = humExt,          windSpeed = wind_speed,
                precipProbability = precipProbability,  dewPoint = dewPoint,        direction = direction,
                uvIndex           = uvIndex,               ozone = ozone,          visibility = visibility,    
                aparent           = aparentTemperature,  sunrise = sunrise,            sunset = sunset)
