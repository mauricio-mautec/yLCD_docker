import configparser
import datetime
import sqlite3
from pathlib import Path
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# CONTROL DATA TYPES STORED IN DATABASE
# GET DATA FROM DATASET
class weatherDB(object):
    database    = "";
    collectData = 0;
    keyMeasured = []
    Measure     = {}

    def getDatabaseName (self):
        if self.database == "":
            here          = Path(__file__).parent / 'weather.ini'
            config        = configparser.ConfigParser()
            config.read   (here)
            self.database = config['database']['weather']
        return self.database

    def setNewCollectData (self, source, location):
        timeNow = datetime.datetime.now()
        conn    = sqlite3.connect (self.getDatabaseName())
        curs    = conn.cursor()
        stmt    = """INSERT INTO collectDataSource VALUES (datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))"""
        curs.execute (stmt, (source, location))
        self.collectData = curs.lastrowid
        conn.commit()

    def saveCollectData (self):
        datavar = self.getData()
        conn    = sqlite3.connect (self.getDatabaseName())
        curs    = conn.cursor()
        stmt    = """INSERT INTO collectData VALUES (?,?,?,?)"""
        import pprint
        print(stmt)
        pprint.pprint(datavar)
        curs.executemany (stmt, datavar)
        conn.commit()
        conn.close()
       
    def resetMeasure(self):
        self.keyMeasured = []
        self.Measure = {
            'humidity'               : ['percent',             0],  
            'pressure'               : ['hPa',                 0], 
            'temperature'            : ['celsius',             0], 
            'temperatureApparent'    : ['celsius',             0],
            'temperatureMax'         : ['celsius',             0], 
            'temperatureMin'         : ['celsius',             0], 
            'temperatureDew'         : ['celsius',             0], 
            'weatherMain'            : ['none',               ''], 
            'weatherDesc'            : ['none',               ''],
            'latitude'               : ['none',                0], 
            'longitude'              : ['none',                0], 
            'windMain'               : ['none',                0], 
            'windSpeed'              : ['km/h',                0],
            'windGust'               : ['km/h',                0],
            'windDegrees'            : ['degrees',             0], 
            'rainIntensity'          : ['in/h',                0],
            'rainProbability'        : ['percent',             0],
            'sunrise'                : ['timestamp',           0], 
            'sunset'                 : ['timestamp',           0],
            'skyUVIndex'             : ['uv',                  0],
            'skyClouds'              : ['percent',             0],
            'skyOzone'               : ['dobson',              0],
            'skyVisibility'          : ['km',                  0],
            'astrodusk'              : ['timestamp',           0],
            'dawn'                   : ['hh:mm:ss',   '00:00:00'],
            'dayLength'              : ['hh:mm:ss',   '00:00:00'],
            'dusk'                   : ['hh:mm:ss',   '00:00:00'],
            'sunRise'                : ['hh:mm:ss',   '00:00:00'],
            'sunSet'                 : ['hh:mm:ss',   '00:00:00'],
            'zenith'                 : ['hh:mm:ss',   '00:00:00'],
            'moonName'               : ['none',               ''],        
            'moonIndex'              : ['none',                0],
            'moonAge'                : ['none',              0.0],
            'moonPhase'              : ['none',               ''],
            'moonDistance'           : ['km',                0.0],
            'moonIllumination'       : ['-',                 0.0],
            'moonAngularDiameter'    : ['-',                 0.0],
            'moonDistanceToSun'      : ['-',                 0.0],
            'sunAngularDiameter'     : ['-',                 0.0]
            }

    def __init__(self, measure):
        self.resetMeasure()
        for medida in measure.keys():
            if medida in self.Measure.keys():
                self.Measure[medida][1] = measure[medida]
        # REMOVE VALUES NOT COLLECT
        if measure:
            keyAvailable = list(self.Measure.keys())
            keyCollected = list(measure.keys()) 
            for key in keyAvailable:
                if key not in keyCollected:
                    val = self.Measure.pop(key, 0)

    def __str__(self):
        result = "\nMeasure CollectData:" + str(self.collectData)  + "\n"
        for medida in self.Measure.keys():
            result += "\n" + medida + ":\t\t " + str(self.Measure[medida][1]) + " " + self.Measure[medida][0]
        return result

    # UPDATE A MEASURE IF IT EXISTS
    def setMeasure (self, measure, value):
        if measure in list(self.Measure.keys()):
            self.Measure[measure][1] = value
            self.keyMeasured.append(measure)

    # REMOVE MEASURE NOT SET       
    def setMeasureClean (self):
        for measure in list(self.Measure.keys()):
            if measure not in self.keyMeasured:
                val = self.Measure.pop(measure, 0)

    # GET A MEASURE IF IT EXISTS
    def getMeasure (self, measure):
        if measure in list(self.Measure.keys()):
            return self.Measure[measure][1]
        else:
            return 0

    # RETURN SQLITE TUPLE FROM DATA COLLECTED
    def getData(self):
        datavar = list()
        for medida in self.Measure.keys():
            unidade = self.Measure[medida][0]
            valor   = self.Measure[medida][1]
            datavar.append((self.collectData, medida, unidade, valor));

        return datavar;

    def getCollectData (self, location, source):
        self.resetMeasure()
        conn  = sqlite3.connect (self.getDatabaseName())
        stmt  = "SELECT ROWID FROM COLLECTDATASOURCE WHERE SOURCE= ? AND LOCATION = ? ORDER BY ROWID DESC LIMIT 1"
        curs  = conn.cursor()
        curs.execute (stmt, (source, location));
        result = curs.fetchone()
        if result is None:
            self.collectData = 0;
            return;
        self.collectData = result[0]
        conn.commit()
        curs  = conn.cursor()
        stmt  = "SELECT MEASURE, VALUE FROM COLLECTDATA WHERE COLLECTDATASOURCE = ? ORDER BY MEASURE"
        curs.execute (stmt, (self.collectData,));
        clima = curs.fetchall()
        keyCollected = []
        keyAvailable = list(self.Measure.keys())
        for medida, valor in clima:
            if medida in keyAvailable:
                self.Measure[medida][1] = valor
                keyCollected.append(medida)
        for key in keyAvailable:
            if key not in keyCollected:
                val = self.Measure.pop(key, 0)

        conn.close()


if __name__ == '__main__':
    print ("THIS FILE SHOULD BE USED AS DATA TRANSFER OBJECT")
    print ("NEW VARIABLES TO BE STORED SHOULD BE CREATED HERE\n")
    print ("dto.py IMPLEMENT CLASS weatherDB\nWITH THE ATTRIBUTES:")
    print ("\tdatabase:    NAME OF SQLITE DATABASE")
    print ("\tcollectData: ID OF COLLECTION")
    print ("\tMeasure:     WEATHER DATA DICT")
    print ("WITH THE METHODS:")
    print ("\tgetCollectData (self, location, source): COLLECT THE LAST DATA FROM LOCATION/TIPO FROM DATABASE")
    print ("\tgetData(self): RETURN TUPLE READY TO BE INSERT IN THE DATABASE")
    print ("\t__str__(self): PRINT DATA SET OF MEASURES")
    print ("\t__init__(self, measure): CREATE INSTANCE WITH measure DATA")
    print ("ACTUAL METADATA WITH TEMPERATURE OF 100:")
    wdb = weatherDB({}) #print (weatherDB({}))
    wdb.setMeasure('temperature', 100)
    print (wdb)
    print ("USING weather.ini")
    here   = Path(__file__).parent / 'weather/weather.ini'
    config = configparser.ConfigParser()
    print(here)
    config.read(here)
    config.sections()
