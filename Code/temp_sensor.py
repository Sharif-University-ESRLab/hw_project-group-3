import os
import glob
import time
from led import *
from math_functions import *
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')

temp_threshold = 26

# temp_sensor_id: led_id 
led_temp_sensor = {
    0: 0,
    1: 1,
    2: 2,
    3: 3
}

def read_temp_raw(device_folder):
    device_file = device_folder + '/w1_slave'

    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def check_all_temp():
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
            print("Sensor {} => {} (C) - {} (F)".format(i + 1, temp_c, temp_f))

    mean, deviations = calc_sd(temps=temps)
    
    deviations_tuples = [(d, temps[i], i) for i, d in enumerate(deviations)]
    deviations_tuples.sort(key=lambda t: t[0], reverse=True)

    hot_sensors_ids = []
    for (sd, temp, id) in deviations_tuples:
        if temp > mean:
            hot_sensors_ids.append(id)
        else:
            break

    for sensor_id in hot_sensors_ids:
        turn_on_led(led_temp_sensor[sensor_id])

    off_sensors = find_complement([0, 1, 2, 3], hot_sensors_ids)

    for sensor_id in off_sensors:
        turn_off_led(led_temp_sensor[sensor_id])


if __name__ == "__main__":
    prep_leds()
    while True:
        check_all_temp()
        time.sleep(1)
