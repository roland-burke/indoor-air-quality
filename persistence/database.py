import os

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime

# You can generate an API token from the "API Tokens Tab" in the UI
token = os.environ['DB_TOKEN']
org = "private"
bucket = "iaq-bucket"
db_url = os.environ['DB_URL']

client = InfluxDBClient(url=db_url, token=token, org=org)

def writePoint(host, description, fieldName, fieldValue):
    point = Point(description).tag("host", host).field(fieldName, fieldValue).time(datetime.datetime.utcnow(), WritePrecision.NS)
    client = None
    try:
        client = InfluxDBClient(url=db_url, token=token, org=org)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket, org, point)
    except Exception as e:
        print("Saving data to '{bucket}' on '{db_url}' failed:", e)
    finally:
        client.close()


def saveTemperature(host, temperature):
    writePoint(host, "indoor_temperature", "temperature", temperature)

def saveHumidity(host, humidity):
    writePoint(host, "indoor_humidity", "humidity", humidity)

def savePressure(host, pressure):
    writePoint(host, "air_pressure", "pressure", pressure)

def saveCo2(host, co2):
    writePoint(host, "co2", "co2", co2)

def saveTvoc(host, tvoc):
    writePoint(host, "tvoc", "tvoc", tvoc)