#!/app/bin/python3
"""
THIS IS THE MAIN ENTRY POINT FOR yLCD
CREATE YOUR APPS AND DISPATCH THEM USING THIS FILE
"""
from   flask                      import Flask, request, render_template
from   dsp.main.displaymain       import DisplayMain
from   dsp.weather.displayweather import DisplayWeather
from   api.weather.weather        import Weather
import sys
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.debug = True # Make this False if you are no longer debugging
@app.route ('/', methods=['GET'])
def hello():
    cidade = request.args.get ('cidade', 'GYN')
    main   = DisplayMain()
    return main.renderDisplay(cidade)

@app.route ("/weather", methods=['GET'])
def weather():
    tipoDisplay  = request.args.get ('tipo', 'none')
    codigo       = request.args.get ('codigo', 'APA')
    logging.debug('yLCD weather tipoDisplay:' + tipoDisplay + ' codigo: ' + codigo)
    display      = DisplayWeather()
    return display.renderDisplay(tipoDisplay, codigo)

@app.route ("/api/weather", methods=['GET'])
def apiWeather():
    tipoInfo     = request.args.get ('tipo', 'none')
    codigo       = request.args.get ('codigo', 'APA')
    logging.debug('yLCD apiWeather tipoInfo:' + tipoInfo + ' codigo: ' + codigo)
    data         = Weather()
    return data.getData(tipoInfo, codigo)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
