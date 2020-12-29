import time
import datetime
import socket
from   dsp.weather.dto import weatherDB
from   flask import request, render_template
import inspect
Cidades = {'SMF' : 'Santa Maria da Feira, PT',
           'GYN' : 'Goiania, BR',
           'CLV' : 'Caldas Novas, BR',
           'APG' : 'Aparecida de Goiania, BR' } 
class DisplayMain:
    # DISPATCH RENDER FRONT END
    def renderDisplay (self, cidade):
        self.IATA   = cidade
        self.cidade = Cidades[cidade]
        return self.display_main()

#    name  = 'varname'
#    value = 'something'
#    setattr(self, name, value) #equivalent to: self.varname= 'something'

    # Convert Degrees to Direction
    def degToCompass(self,num):
        val=int((num/22.5)+.5)
        arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
        return arr[(val % 16)]

    # DEFAULT FRONT END DISPLAY
    # TEMPLATE display_main.html 
    def display_main(self):
        # Calendar & Host info
        horario = time.strftime ("%H:%M")
        calMes  = time.strftime ("%b")
        calWek  = time.strftime ("%a");
        calDay  = time.strftime ("%d");

        Tempo    = "{a} {b} {c} {d}".format(a=horario, b=calMes, c=calWek, d=calDay)
        hostName = socket.gethostname()
        hostIP   = socket.gethostbyname ("rbpidisplay")

        # Inside Home Weather Info
        wdb     = weatherDB ({})
        wdb.getCollectData ('Home GYN', 'RBPI Weather Station')
        tempLab = wdb.getMeasure('temperature')
        humLab  = wdb.getMeasure('humidity')   


        wdb.getCollectData (self.cidade, 'darksky.net')
        dadosDSK = wdb.getData()
        dadosDSK.sort()
        
        wdb.getCollectData (self.cidade, 'openweathermap.org')
        dadosOWM = wdb.getData()
        dadosOWM.sort()
        
        wdb.getCollectData (self.cidade, 'yr.no')
        dadosYR = wdb.getData()
        dadosYR.sort()
     
        Temp = 0
        Hum  = 0
        for code,medida,unidade,valor in dadosDSK:
            if medida == 'temperature':
                Temp += valor;
            if medida == 'humidity':
                Hum += valor;

        for code,medida,unidade,valor in dadosOWM:
            if medida == 'temperature':
                Temp += valor;
            if medida == 'humidity':
                Hum += valor;

        for code,medida,unidade,valor in dadosYR: 
            if medida == 'temperature':
                Temp += valor;

        Temp /= 3.0
        Hum  /= 2.0

    # DEFAULT FRONT END DISPLAY
    # TEMPLATE display_main.html 
        template = 'main/' + inspect.currentframe().f_code.co_name + ".html"
        return render_template (template, infoDSK = dadosDSK, infoOWM = dadosOWM, infoYR = dadosYR,
                                IATA = self.IATA, TEMPO = Tempo, TEMP = Temp, HUM = Hum, TEMPLAB = tempLab, HUMLAB = humLab)
