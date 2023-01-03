import RPi.GPIO as GPIO
import time


led_id_pin = {
    0: 5,
    1: 6,
    2: 13,
    3: 19,
}

def turn_on_led(led_id):
    GPIO.output(led_id_pin[led_id], GPIO.HIGH)
    print("LED {} on".format(led_id))


def turn_off_led(led_id):
    GPIO.output(led_id_pin[led_id], GPIO.LOW)
    print("LED {} off".format(led_id))

def prep_leds():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for pin in led_id_pin.values():
        print(pin)
        GPIO.setup(pin, GPIO.OUT)

def test_leds():
    while True():
        turn_off_led(3)
        turn_on_led(0)
        time.sleep(1)

        turn_off_led(0)
        turn_on_led(1)
        time.sleep(1)

        turn_off_led(1)
        turn_on_led(2)
        time.sleep(1)
        
        turn_off_led(2)
        turn_on_led(3)
        time.sleep(1)


if __name__ == '__main__':
    prep_leds()
    test_leds()

