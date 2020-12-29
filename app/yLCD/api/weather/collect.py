import configparser
import requests
import time
from   pathlib     import Path
from   dsp.weather.dto import weatherDB
from   dsp.weather.location import *
from   darksky     import forecast
from   yr.libyr    import Yr
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#clima = weather.now(as_json=True)

# TRANSLATOR FOR DATA COMMING FROM YR
class YR():
    wdb = weatherDB({})

    def __init__(self, codigo):
        site       = locationSite(codigo)
        weather    = Yr(site)
        main       = weather.now()
        if (main):
            self.wdb.setMeasure('pressure'        , main['pressure']     ['@value']    )
            self.wdb.setMeasure('temperature'     , main['temperature']  ['@value']    )
            self.wdb.setMeasure('weatherMain'     , main['symbol']       ['@name']     )
            self.wdb.setMeasure('windSpeed'       , float(main['windSpeed']    ['@mps']) * 3.6)
            self.wdb.setMeasure('windMain'        , main['windSpeed']     ['@name']     )
            self.wdb.setMeasure('windDegrees'     , main['windDirection']['@deg']      )
            self.wdb.setMeasure('rainProbability' , main['precipitation']['@value']    )
            self.wdb.setMeasureClean()

# TRANSLATOR FOR DATA COMMING FROM DARKSKY
class DarkSky():
    wdb = weatherDB({})
    
    def __init__(self, apiKey, codigo):
        site, self.latitude, self.longitude  = locationSiteCoordenate(codigo)
        
        if self.latitude != 0 and self.longitude != 0:
            fcast = forecast(apiKey, self.latitude, self.longitude, units='si')
        else:
            fcast = []
 
        if (fcast): 
            main  = fcast.currently
            self.wdb.setMeasure('humidity'           ,main.humidity * 100)
            self.wdb.setMeasure('pressure'           ,main.pressure)
            self.wdb.setMeasure('temperature'        ,main.temperature)
            self.wdb.setMeasure('temperatureApparent',main.apparentTemperature)
            self.wdb.setMeasure('temperatureDew'     ,main.dewPoint)
            self.wdb.setMeasure('weatherMain'        ,main.summary)
            self.wdb.setMeasure('latitude'           ,self.latitude )
            self.wdb.setMeasure('longitude'          ,self.longitude)
            self.wdb.setMeasure('windSpeed'          ,main.windSpeed * 3.6)
            self.wdb.setMeasure('windGust'           ,main.windGust * 3.6)
            self.wdb.setMeasure('windDegrees'        ,main.windBearing )
            self.wdb.setMeasure('rainIntensity'      ,main.precipIntensity)
            self.wdb.setMeasure('rainProbability'    ,main.precipProbability * 100)
            self.wdb.setMeasure('skyUVIndex'         ,main.uvIndex)
            self.wdb.setMeasure('skyClouds'          ,main.cloudCover * 100)
            self.wdb.setMeasure('skyOzone'           ,main.ozone)
            self.wdb.setMeasure('skyVisibility'      ,main.visibility )
            self.wdb.setMeasureClean()
            

# TRANSLATOR FOR DATA COMMING FROM OPENWEATHERMAP
class OpenWeatherMap():
    wdb  = weatherDB({});
    
    def __init__(self, apiKey, codigo):
        location = locationCity(codigo)
        url      = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(location, apiKey)
        result   = requests.get(url)
        clima    = result.json()
        weather  = clima['weather'][0]
        main     = clima['main']
        clouds   = clima['clouds']
        cldkey   = [x for x in clouds.keys()][0]
        cldval   = clouds[cldkey]
        coord    = clima['coord']
        wind     = clima['wind']
        speed    = 0
        deg      = 0
        if 'speed' in wind: speed = wind['speed']
        if 'deg'   in wind: deg   = wind['deg']
        sys      = clima['sys']

        self.wdb.setMeasure('humidity'           ,main['humidity'])
        self.wdb.setMeasure('pressure'           ,main['pressure'])
        self.wdb.setMeasure('temperature'        ,main['temp'])
        self.wdb.setMeasure('temperatureMax'     ,main['temp_max'])
        self.wdb.setMeasure('temperatureMin'     ,main['temp_min'])
        self.wdb.setMeasure('weatherMain'        ,weather['main'])
        self.wdb.setMeasure('weatherDesc'        ,weather['description'])
        self.wdb.setMeasure('latitude'           ,coord['lat'])
        self.wdb.setMeasure('longitude'          ,coord['lon'])
        self.wdb.setMeasure('skyClouds'          ,cldval)
        if 'visibility' in clima:
            self.wdb.setMeasure('skyVisibility'      ,clima['visibility'] / 1000)
        self.wdb.setMeasure('windSpeed'          ,speed * 3.6)
        self.wdb.setMeasure('windDegrees'        ,deg)
        self.wdb.setMeasure('sunrise'            ,sys['sunrise'])
        self.wdb.setMeasure('sunset'             ,sys['sunset'])
        self.wdb.setMeasureClean()

# TRANSLATOR FOR DATA COMMING FROM FARMSENSE
class FarmSense():
    wdb  = weatherDB({});
    
    def __init__(self, codigo):
        location, latitude, longitude = locationSiteCoordenate(codigo)
        timestp  = int(time.time())
        url      = f"https://api.farmsense.net/v1/daylengths/?d={timestp}&lat={latitude}&lon={longitude}"
        result   = requests.get(url)
        clima    = result.json()
        main     = clima[0]
        if main['ErrorMessage'] == '': 
            self.wdb.setMeasure('astrodusk'  ,main['Astrodusk'])
            self.wdb.setMeasure('dawn'       ,main['Dawn'])
            self.wdb.setMeasure('dayLength'  ,main['Daylength'])
            self.wdb.setMeasure('dusk'       ,main['Dusk'])
            self.wdb.setMeasure('sunRise'    ,main['Sunrise'])
            self.wdb.setMeasure('sunSet'     ,main['Sunset'])
            self.wdb.setMeasure('zenith'     ,main['Zenith'])
        url      = f"https://api.farmsense.net/v1/moonphases/?d={timestp}"
        result   = requests.get(url)
        clima    = result.json()
        main     = clima[0]
        if main['ErrorMsg'] == 'success': 
            self.wdb.setMeasure('moonName'           ,main['Moon'][0])
            self.wdb.setMeasure('moonIndex'          ,main['Index'])
            self.wdb.setMeasure('moonAge'            ,main['Age'])
            self.wdb.setMeasure('moonPhase'          ,main['Phase'])
            self.wdb.setMeasure('moonDistance'       ,main['Distance'])
            self.wdb.setMeasure('moonIllumination'   ,main['Illumination'])
            self.wdb.setMeasure('moonAngularDiameter',main['AngularDiameter'])
            self.wdb.setMeasure('moonDistanceToSun'  ,main['DistanceToSun'])
            self.wdb.setMeasure('sunAngularDiameter' ,main['SunAngularDiameter'])
        self.wdb.setMeasureClean()

# COLLECT DATA FROM SOURCES
class WeatherCollector():
    def __init__(self, source):
        self.source    = source
        self.codigo    = ""
        self.latitude  = 0
        self.longitude = 0

        # API KEYS
        here        = Path(__file__).parent / 'weather.ini'
        config      = configparser.ConfigParser()
        config.read (here)

        if self.source in config:
            self.apiKey = config[self.source]['apikey']
        else:
            print ("API KEY NOT FOUND FOR SOURCE: {}".format(self.source))
            print ("SOURCE AVAILBLE: darksky.net, openweathermap.org, yr.no")
            raise Exception()

    def __str__(self):
        return ("DataSource:{} APIKey:{}".format(self.source, self.apiKey))

    def saveWeather (self):
        if self.codigo != "" and self.dados:
            self.dados.wdb.setNewCollectData(self.source, self.codigo)
        
        if self.dados.wdb.collectData != 0:
            self.dados.wdb.saveCollectData()

    # RETURN DATA IN A WEATHERDB OBJECT
    def getWeather (self, codigo):
        # CURRENT SOURCES AND TRANSLATORS
        if self.source == 'darksky.net':
            self.dados  = DarkSky (self.apiKey, codigo)
        elif self.source == 'openweathermap.org':
            self.dados  = OpenWeatherMap(self.apiKey, codigo)
        elif self.source == 'yr.no':
            self.dados  = YR(codigo)
        elif self.source == 'farmsense.net':
            self.dados = FarmSense(codigo)
        else:
            self.dados = {}

        # RETURN COLLECTED DATA
        if self.dados:
            self.codigo = codigo
            return self.dados.wdb
        else:
            self.codigo = ""
            return weatherDB ({})
