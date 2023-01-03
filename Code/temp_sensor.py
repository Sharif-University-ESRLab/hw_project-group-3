import os
import glob
import time
from led import *
from math_functions import *
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# directory which the data of sensors ar written in
base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')

# dictionary for mapping temp_sensor_id to led_id 
led_temp_sensor = {
    0: 0,
    1: 1,
    2: 2,
    3: 3
}

# reads temperatures for each sensor
def read_temp_raw(device_folder):
    device_file = device_folder + '/w1_slave'

    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# checks the temperatures and turns on the cooler of needed for the exposed sensor
def check_all_temp(exposed_sensor):
    temps = []
    for i, df in enumerate(device_folders):
        lines = read_temp_raw(df)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            temps.append(temp_c)
            print("Sensor {} => {} (C) - {} (F)".format(i, temp_c, temp_f))

    # mean of all the temps
    mean, deviations = calc_sd(temps=temps)

    # id of the hot sensors which have a temperature at least 1 degree above mean
    hot_sensors_ids = []

    for i, t in enumerate(temps):
        if t - mean >= 1:
            hot_sensors_ids.append(i)

    for sensor_id in hot_sensors_ids:
        if sensor_id == exposed_sensor:
            # turn on the exposed sensor if it is at least 1 degree hotter that the mean temperature
            turn_on_led(led_temp_sensor[sensor_id])
        else:
            turn_off_led(led_temp_sensor[sensor_id])

    # sensors which have to be turned off
    off_sensors = find_complement([0, 1, 2, 3], hot_sensors_ids)

    for sensor_id in off_sensors:
        turn_off_led(led_temp_sensor[sensor_id])

