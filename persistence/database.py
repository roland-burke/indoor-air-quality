from json.tool import main
from time import sleep

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime

# You can generate an API token from the "API Tokens Tab" in the UI
token = "my-super-secret-auth-token"
org = "private"
bucket = "iaq-bucket"
db_url = "http://localhost:8086"

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

def savePressure(host, humidity):
    point = Point("air_pressure").tag("host", host).field("pressure", humidity).time(datetime.datetime.utcnow(), WritePrecision.NS)
    writePoint(point)