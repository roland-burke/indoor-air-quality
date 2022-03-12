from pickle import NONE
from time import sleep
import database
import urllib.request
import json
import os

client_url = os.environ['DATA_URL']
INTERVAL = 2 # in seconds

def saveToDatabase(host, temperature, humidity, pressure, co2, tvoc):
    database.saveTemperature(host, temperature)
    database.saveHumidity(host, humidity)
    database.savePressure(host, pressure)
    database.saveCo2(host, co2)
    database.saveTvoc(host, tvoc)

def fetchDataFromClient():
    try:
        response = urllib.request.urlopen(client_url).read()
        return json.loads(response.decode('utf-8'))
    except Exception as e:
        print("Fetch data from {data_url} failed:", e)
        return None


def fetchAndSave():
    while(True):
        data = fetchDataFromClient()
        if data != None:
            saveToDatabase(data['hostname'], data['temperature'], data['humidity'], data['pressure'], data['co2'], data['tvoc'])
        else:
            print("No data was saved")
        sleep(INTERVAL)

if __name__ == '__main__':
    fetchAndSave()
