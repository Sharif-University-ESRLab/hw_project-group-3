import serial
import time
import string
import pynmea2
import numpy as np
from suncalc import get_position
from datetime import datetime, timezone
from test import get_coordinates_manual
from led import prep_leds
from temp_sensor import check_all_temp

# function for reading the coordinates of the buffer
def main():
    while True:
        port = "/dev/ttyAMA0" # where the data is written gotten from GPS sensor
        ser = serial.Serial(port, baudrate=9600, timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()
        data1 = ser.readline()
        current_time = time.time()

		# reading the data which show the latitude and longitude
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

			# coordinates of the first spot
			lat1 = msg1.latitude
			lng1 = msg2.longitude

			# coordinates of the second spot
			lat2 = msg2.latitude
			lng2 = msg2.longitude

			# getting the direction of the path between first and second spot
			angle_from_north = np.arctan2(np.sin(lng2 - lng1), np.sin(lat2 - lat1))
			date = datetime.now(timezone.utc)

			# calculating the sun position and its angle with our current position
			sun_pos = get_position(date, lng2, lat2)
			sun_angle = (sun_pos['azimuth'] - angle_from_north) % (2 * np.pi)

			# exposed sensor: the temp sensor in car which is exposed to the sun
			exposed_sensor = None
			if sun_angle < np.pi / 2:
					exposed_sensor = 2 # front-right
			elif sun_angle < np.pi:
					exposed_sensor = 3 # back-right
			elif sun_angle < 3 * np.pi / 2:
					exposed_sensor = 1 # back-left
			else:
					exposed_sensor = 0 # front-left

			print("sensor", exposed_sensor, " is close to the Sun.")

		    # here we check all the tempretures and if the highest temp is for the exposed sensor, we turn the cooler on
			check_all_temp(exposed_sensor)



# manually we change the direction of the car
def manual_main():
    curr_lat = 35.703129
    curr_long = 51.351671

    while True:
        start_lat, start_long, curr_lat, curr_long = get_coordinates_manual(curr_lat, curr_long, direction='E', step=0.001)

		# coordinates of the first spot
        lat1 = start_lat
        lng1 = start_long

		# coordinates of the second spot
        lat2 = curr_lat
        lng2 = curr_long
        print(lat1, lng1, lat2, lng2, np.sin(lng2 - lng1), np.sin(lat2 - lat1))
        angle_from_north = np.arctan2(np.sin(lng2 - lng1), np.sin(lat2 - lat1))
        date = datetime.now(timezone.utc)

        sun_pos = get_position(date, lng2, lat2)
        sun_angle = (sun_pos['azimuth'] - angle_from_north) % (2 * np.pi)

        print("Movement Direction:", angle_from_north, ",Sun Azimuth:", sun_pos['azimuth'], ",Sun Angle:", sun_angle)

        if sun_angle < np.pi / 2:
            exposed_sensor = 2
        elif sun_angle < np.pi:
            exposed_sensor = 3
        elif sun_angle < 3 * np.pi / 2:
            exposed_sensor = 1
        else:
            exposed_sensor = 0

        print("Sensor", exposed_sensor, " is close to the Sun.")

		# here we check all the temperatures and if the highest temp is for the exposed sensor, we turn the cooler on
        check_all_temp(exposed_sensor)

        time.sleep(1)


if __name__ == "__main__":
	# we initialize the LEDs at the beginning
	prep_leds()

	#main()
	manual_main()
