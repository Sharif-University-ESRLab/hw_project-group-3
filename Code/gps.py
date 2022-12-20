import serial
import time
import string
import pynmea2
import numpy as np
from suncalc import get_position
from datetime import datetime
#import astropy.coordinates as coord
#from astropy.time import Time
#import astropy.units as u

def calculate_solar_angle(latitude, longtitude):
    loc = coord.EarthLocation(lon=longtitude * u.deg, lat=latitude * u.deg)
    now = Time.now()
    altaz = coord.AltAz(location=loc, obstime=now)
    sun = coord.get_sun(now)
    return sun.transform_to(altaz).alt

while True:
    port = "/dev/ttyAMA0"
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    data1 = ser.readline()
    current_time = time.time()

    if data1[0:6] == b'$GPRMC':

        data2= None
        while time.time() - current_time < 5:
            newdata = ser.readline()
            if newdata[0:6] == b'$GPRMC' and time.time() - current_time > 1:
                data2 = newdata
                break

        if not data2:
            print("timeout!")
            continue

        data1 = str(data1)[2:-5]
        data2 = str(data2)[2:-5]

        msg1 = pynmea2.parse(data1)
        msg2 = pynmea2.parse(data2)

        lat1 = msg1.latitude
        lng1 = msg2.longitude

        lat2 = msg2.latitude
        lng2 = msg2.longitude

        angle_from_north = np.arctan(np.sin((lng2 - lng1) / 2) / np.sin((lat2 -                                                                                                                                    lat1) / 2))

        date = datetime.now()
        sun_pos = get_position(date, lng2, lat2)

        loc = "Latitude=" + str(lat2) + "and Longitude=" + str(lng2) + "\nAzimut                                                                                                                                   h=" + atr(sun_pos[azimuth]) + "Sun Angle=" + str(angle_from_north * 180 / no.pi                                                                                                                                    - sun_pos[azimuth])
        print(loc)
