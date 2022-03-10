from time import sleep
import database
import urllib.request
import json
import os

data_url = os.environ['DATA_URL']

def saveToDabase(host, temperature, humidity, pressure, co2, tvoc):
    try:
        database.saveTemperature(host, temperature)
        database.saveHumidity(host, humidity)
        database.savePressure(host, pressure)
        database.saveCo2(host, co2)
        database.saveTvoc(host, tvoc)

    except Exception as e:
        print("Saving data failed:", e)

def start():
    while(True):

        try:
            response = urllib.request.urlopen(data_url).read()
            jsonResponse = json.loads(response.decode('utf-8'))
            host = jsonResponse['hostname']
            #print(jsonResponse)
            print("Host:", host)
            print("Received temperature:", jsonResponse['temperature'])
            print("Received humidity:", jsonResponse['humidity'])
            print("Received pressure:", jsonResponse['pressure'])
            saveToDabase(host, jsonResponse['temperature'], jsonResponse['humidity'], jsonResponse['pressure'], jsonResponse['co2'], jsonResponse['tvoc'])
        except Exception as e:
            print("Read data failed:", e)


        sleep(2)
start()