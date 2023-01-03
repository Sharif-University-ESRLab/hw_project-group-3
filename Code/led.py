import RPi.GPIO as GPIO
import time


# dictionary which maps LED id to its corresponding GPIO pin
led_id_pin = {
    0: 5,
    1: 6,
    2: 13,
    3: 19,
}

# function for turning on the LED given the id
def turn_on_led(led_id):
    GPIO.output(led_id_pin[led_id], GPIO.HIGH)
    print("LED {} on".format(led_id))


# function for turning off the LED given the id
def turn_off_led(led_id):
    GPIO.output(led_id_pin[led_id], GPIO.LOW)
    print("LED {} off".format(led_id))

# initializes the LED pins on raspberry pi
def prep_leds():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for pin in led_id_pin.values():
        GPIO.setup(pin, GPIO.OUT)

