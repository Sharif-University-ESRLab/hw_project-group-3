import serial
import time
import string
import pynmea2
import astropy.coordinates as coord
from astropy.time import Time
import astropy.units as u

def calculate_solar_angle(latitude, longtitude):
    loc = coord.EarthLocation(lon=longtitude * u.deg, lat=latitude * u.deg)
    now = Time.now()

    altaz = coord.AltAz(location=loc, obstime=now)
    sun = coord.get_sun(now)

    return sun.transform_to(altaz).alt


while True:
	port="/dev/ttyAMA0"
	ser=serial.Serial(port, baudrate=9600, timeout=0.5)
	dataout = pynmea2.NMEAStreamReader()
	newdata=ser.readline()

	if newdata[0:6] == "$GPRMC":
		newmsg=pynmea2.parse(newdata)
		lat=newmsg.latitude
		lng=newmsg.longitude
		gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
		print(gps)

        solar_angle = calculate_solar_angle(lat, lng)
        print("Solar Angle: {}".format(solar_angle))
