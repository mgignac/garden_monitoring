#!/usr/bin/python3

import influxdb

import Adafruit_BMP.BMP085 as BMP085

sensor = BMP085.BMP085(busnum=1)

print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))

# build an influxDB points dictionary for the values to record
points = [
    {
        "measurement": "local-pressure",
        "tags": {},
        "fields": dict(value=float(sensor.read_pressure()/1000.0)),
    },
    {
        "measurement": "altitude",
        "tags": {},
        "fields": dict(value=sensor.read_altitude()),
    },
    {
        "measurement": "sea-pressure",
        "tags": {},
        "fields": dict(value=float(sensor.read_sealevel_pressure()/1000.0)),
    },
    
]

print(points)

# make an influxdb client
client = influxdb.InfluxDBClient(
    host="localhost",
    port=1234,
    gzip=True,
)
# send the data to influxdb
success = client.write_points(
    points,
    time_precision="s",
    database="db0",
    tags={
        "project": "garden",
        "model": "Pressure",
        "location": "main",
    },
)


