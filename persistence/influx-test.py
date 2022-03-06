from json.tool import main
from time import sleep

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime

# You can generate an API token from the "API Tokens Tab" in the UI
token = "my-super-secret-auth-token"
org = "private"
bucket = "iaq-bucket"

curr_time = datetime.datetime.utcnow()

def init():
	client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)
	return client


def addTemperature(client):
	write_api = client.write_api(write_options=SYNCHRONOUS)

	point = Point("indoor_temperature").tag("host", "pi-zero").field("temperature", 22.45).time((curr_time - datetime.timedelta(0,40)), WritePrecision.NS)
	write_api.write(bucket, org, point)
	point = Point("indoor_temperature").tag("host", "pi-zero").field("temperature", 22.89).time((curr_time - datetime.timedelta(0,35)), WritePrecision.NS)
	write_api.write(bucket, org, point)
	point = Point("indoor_temperature").tag("host", "pi-zero").field("temperature", 23.21).time((curr_time - datetime.timedelta(0,30)), WritePrecision.NS)
	write_api.write(bucket, org, point)

	point = Point("indoor_temperature").tag("host", "pi-zero").field("temperature", 23.14).time((curr_time - datetime.timedelta(0,25)), WritePrecision.NS)
	write_api.write(bucket, org, point)
	point = Point("indoor_temperature").tag("host", "pi-zero").field("temperature", None).time((curr_time - datetime.timedelta(0,20)), WritePrecision.NS)
	write_api.write(bucket, org, point)

	point = Point("indoor_temperature").tag("host", "pi-zero").field("temperature", 23.10).time((curr_time - datetime.timedelta(0,15)), WritePrecision.NS)
	write_api.write(bucket, org, point)
	point = Point("indoor_temperature").tag("host", "pi-zero").field("temperature", 23.00).time((curr_time - datetime.timedelta(0,10)), WritePrecision.NS)
	write_api.write(bucket, org, point)
	point = Point("indoor_temperature").tag("host", "pi-zero").field("temperature", 22.60).time((curr_time - datetime.timedelta(0,5)), WritePrecision.NS)
	write_api.write(bucket, org, point)

def addHumidity(client):
	write_api = client.write_api(write_options=SYNCHRONOUS)
	point = Point("indoor_humidity").tag("host", "pi-zero").field("humidity", 38).time((curr_time - datetime.timedelta(0,30)), WritePrecision.NS)
	write_api.write(bucket, org, point)
	point = Point("indoor_humidity").tag("host", "pi-zero").field("humidity", 40).time((curr_time - datetime.timedelta(0,25)), WritePrecision.NS)
	write_api.write(bucket, org, point)
	point = Point("indoor_humidity").tag("host", "pi-zero").field("humidity", 45).time((curr_time - datetime.timedelta(0,20)), WritePrecision.NS)
	write_api.write(bucket, org, point)

	point = Point("indoor_humidity").tag("host", "pi-zero").field("humidity", 44).time((curr_time - datetime.timedelta(0,15)), WritePrecision.NS)
	write_api.write(bucket, org, point)
	point = Point("indoor_humidity").tag("host", "pi-zero").field("humidity", 42).time((curr_time - datetime.timedelta(0,10)), WritePrecision.NS)
	write_api.write(bucket, org, point)
	point = Point("indoor_humidity").tag("host", "pi-zero").field("humidity", 42).time((curr_time - datetime.timedelta(0,5)), WritePrecision.NS)
	write_api.write(bucket, org, point)

def addPressure(client):
	write_api = client.write_api(write_options=SYNCHRONOUS)
	point = Point("air_pressure").tag("host", "pi-zero").field("pressure", 1060.5).time((curr_time - datetime.timedelta(0,30)), WritePrecision.NS)
	write_api.write(bucket, org, point)
	point = Point("air_pressure").tag("host", "pi-zero").field("pressure", 1060.7).time((curr_time - datetime.timedelta(0,25)), WritePrecision.NS)
	write_api.write(bucket, org, point)
	point = Point("air_pressure").tag("host", "pi-zero").field("pressure", 1061.0).time((curr_time - datetime.timedelta(0,20)), WritePrecision.NS)
	write_api.write(bucket, org, point)

	point = Point("air_pressure").tag("host", "pi-zero").field("pressure", 1060.7).time((curr_time - datetime.timedelta(0,15)), WritePrecision.NS)
	write_api.write(bucket, org, point)
	point = Point("air_pressure").tag("host", "pi-zero").field("pressure", 1060.6).time((curr_time - datetime.timedelta(0,10)), WritePrecision.NS)
	write_api.write(bucket, org, point)
	point = Point("air_pressure").tag("host", "pi-zero").field("pressure", 1060.3).time((curr_time - datetime.timedelta(0,5)), WritePrecision.NS)
	write_api.write(bucket, org, point)

if __name__ == '__main__':
	client = init()

	print(curr_time)

	addTemperature(client)
	addHumidity(client)
	addPressure(client)

	client.close()
	
	
