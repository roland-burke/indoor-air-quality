from time import sleep
import database
import urllib.request
import json

url = "http://localhost:5000/api/data"

def start():
    while(True):

        try:
            response = urllib.request.urlopen(url).read()
            jsonResponse = json.loads(response.decode('utf-8'))
            #print(jsonResponse)
            print("Host:", jsonResponse['hostname'])
            print("Received temperature:", jsonResponse['temperature'])
            print("Received humidity:", jsonResponse['humidity'])
            print("Received pressure:", jsonResponse['pressure'])
        except Exception as e:
            print("Read data failed:", e)



        #database.saveTemperature("host", 22.9)
        sleep(2)
start()