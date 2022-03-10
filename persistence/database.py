from json.tool import main
from time import sleep
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

def writePoint(point):
    client = InfluxDBClient(url=db_url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket, org, point)
    client.close()

def saveTemperature(host, temperature):
    point = Point("indoor_temperature").tag("host", host).field("temperature", temperature).time(datetime.datetime.utcnow(), WritePrecision.NS)
    writePoint(point)

def saveHumidity(host, humidity):
    point = Point("indoor_humidity").tag("host", host).field("humidity", humidity).time(datetime.datetime.utcnow(), WritePrecision.NS)
    writePoint(point)

def savePressure(host, pressure):
    point = Point("air_pressure").tag("host", host).field("pressure", pressure).time(datetime.datetime.utcnow(), WritePrecision.NS)
    writePoint(point)

def saveCo2(host, co2):
    point = Point("co2").tag("host", host).field("co2", co2).time(datetime.datetime.utcnow(), WritePrecision.NS)
    writePoint(point)

def saveTvoc(host, tvoc):
    point = Point("co2").tag("host", host).field("tvoc", tvoc).time(datetime.datetime.utcnow(), WritePrecision.NS)
    writePoint(point)