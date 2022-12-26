import serial
import time
import string
import pynmea2
import numpy as np
from suncalc import get_position
from datetime import datetime
from test import get_coordinates_manual
#import astropy.coordinates as coord
#from astropy.time import Time
#import astropy.units as u

#def calculate_solar_angle(latitude, longtitude):
#    loc = coord.EarthLocation(lon=longtitude * u.deg, lat=latitude * u.deg)
#    now = Time.now()
#    altaz = coord.AltAz(location=loc, obstime=now)
#    sun = coord.get_sun(now)
#    return sun.transform_to(altaz).alt

def main():
	while True:
		port = "/dev/ttyAMA0"
		ser = serial.Serial(port, baudrate=9600, timeout=0.5)
		dataout = pynmea2.NMEAStreamReader()
		data1 = ser.readline()
		current_time = time.time()

		if data1[0:6] == b'$GPRMC':

			data2= None
			while time.time() - current_time < 20:
				newdata = ser.readline()
				if newdata[0:6] == b'$GPRMC' and time.time() - current_time > 5:
					data2 = newdata
					break

			if not data2:
				print("timeout!")
				continue

			data1 = str(data1)[2:-5]
			data2 = str(data2)[2:-5]
			print(data1, data2)
			msg1 = pynmea2.parse(data1)
			msg2 = pynmea2.parse(data2)

			lat1 = msg1.latitude
			lng1 = msg2.longitude

			lat2 = msg2.latitude
			lng2 = msg2.longitude
			x = (lng2 - lng1) / (lat2 - lat1)
			angle_from_north = np.arctan((lng2 - lng1) / (lat2 - lat1))
			print(lat1, lng1, lat2, lng2, x, angle_from_north)
			date = datetime.now()
			sun_pos = get_position(date, lng2, lat2)

			loc = "Latitude=" + str(lat2) + "and Longitude=" + str(lng2) + "\nAzimuth=" + str(sun_pos['azimuth']) + ",Sun Angle=" + str(angle_from_north * 180 / np.pi - sun_pos['azimuth'])
			print(loc)

def manual_main():
	curr_lat = 35.703129
	curr_long = 51.351671

	while True:
        start_lat, start_long, curr_lat, curr_long = get_coordinates_manual(curr_lat, curr_long)

	    lat1 = start_lat
		lng1 = start_long

		lat2 = curr_lat
		lng2 = curr_long
		x = (lng2 - lng1) / (lat2 - lat1)
		angle_from_north = np.arctan((lng2 - lng1) / (lat2 - lat1))
		print(lat1, lng1, lat2, lng2, x, angle_from_north)
		date = datetime.now()
		sun_pos = get_position(date, lng2, lat2)

		loc = "Latitude=" + str(lat2) + "and Longitude=" + str(lng2) + "\nAzimuth=" + str(sun_pos['azimuth']) + ",Sun Angle=" + str(angle_from_north * 180 / np.pi - sun_pos['azimuth'])
		print(loc)

		time.sleep(5)


if __name__ == "__main__":
	#main()
	manual_main()
