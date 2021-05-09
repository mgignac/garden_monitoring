import time
import board
import adafruit_dht


import influxdb


#Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D17)
# Print the values to the serial port
temperature_c = dhtDevice.temperature
temperature_f = temperature_c * (9 / 5) + 32
humidity = dhtDevice.humidity
print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))

points = [
    {
        "measurement": "humidity",
        "tags": {},
        "fields": dict(value=humidity),
    },
    {
        "measurement": "temperature",
        "tags": {},
        "fields": dict(value=temperature_c),
    },
]

print(points)

# make an influxdb client
client = influxdb.InfluxDBClient(
    host="localhost",
    port=1234,
    #ssl=True,
    #username='user', password='password',
    #verify_ssl=True,
    #path="influxdb",
    gzip=True,
)
# send the data to influxdb
success = client.write_points(
    points,
    time_precision="s",
    database="db0",
    tags={
        "project": "garden",
        "model": "DTH11",
        "location": "main",
    },
)



