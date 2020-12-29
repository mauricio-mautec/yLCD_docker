locationDict = {
        'SMF': ['Santa Maria da Feira, PT'  ,'Portugal/Aveiro/Feira',              40.927100, -8.5495000],
        'GYN': ['Goiania, BR'               ,'Brazil/Goiás/Goiânia',              -16.701028, -49.266793],
        'APA': ['Aparecida de Goiania, BR'  ,'Brazil/Goiás/Aparecida de Goiânia', -16.829400, -49.295300],
        'CLV': ['Caldas Novas, BR'          ,'Brazil/Goiás/Caldas Novas',         -17.745000, -48.622500],
        'GRU': ['Sao Paulo, BR'             ,'Brazil/São Paulo/São Paulo',        -23.550000, -46.640000],
        'VCP': ['Campinas, BR'              ,'Brazil/São Paulo/Campinas',         -22.910000, -47.060000],
        'BSB': ['Brasilia, BR'              ,'Brazil/Distrito Federal/Brasilia',  -15.780000, -47.930000],
        }
    
def locationCity(codigo):
    if codigo in locationDict.keys():
        return locationDict[codigo][0]
    else:
        return 'Aparecida de Goiania, BR'

def locationSite(codigo):
    if codigo in locationDict.keys():
        return locationDict[codigo][1]

def locationSiteCoordenate(codigo):
    if codigo in locationDict.keys():
        return [locationDict[codigo][1], locationDict[codigo][2], locationDict[codigo][3]]
