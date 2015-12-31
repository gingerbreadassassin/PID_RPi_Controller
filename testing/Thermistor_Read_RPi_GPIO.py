#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  temp_LED.py
#
# Use a thermistor to read temperatures and illuminate
# a number of LEDs based upon the returned temperature
#
#  Copyright 2015  Ken Powers
#

import time, math
import RPi.GPIO as GPIO

# Set GPIO pins to Broadcom numbering system
GPIO.setmode(GPIO.BCM)

# Define our constants
RUNNING = True
led_list = [17,27,22,10,9,11,13,26] # GPIO pins for LEDs
temp_low = 70 # Lowest temperature for LEDs (F)
temp_high = 86 # Highest temperature for LEDs (F)
a_pin = 23
b_pin = 24

# Set up our LED GPIO pins as outputs
for x in range(0,8):
    GPIO.setup(led_list[x], GPIO.OUT)
    GPIO.output(led_list[x], GPIO.LOW)

# Try to keep this value near 1 but adjust it until
# the temperature readings match a known thermometer
adjustment_value = 0.97

# Create a function to take an analog reading of the
# time taken to charge a capacitor after first discharging it
# Perform the procedure 100 times and take an average
# in order to minimize errors and then convert this
# reading to a resistance
def resistance_reading():
    total = 0
    for i in range(1, 100):
        # Discharge the 330nf capacitor
        GPIO.setup(a_pin, GPIO.IN)
        GPIO.setup(b_pin, GPIO.OUT)
        GPIO.output(b_pin, False)
        time.sleep(0.01)
        # Charge the capacitor until our GPIO pin
        # reads HIGH or approximately 1.65 volts
        GPIO.setup(b_pin, GPIO.IN)
        GPIO.setup(a_pin, GPIO.OUT)
        GPIO.output(a_pin, True)
        t1 = time.time()

        while not GPIO.input(b_pin):
            pass
        t2 = time.time()

        # Record the time taken and add to our total for
        # an eventual average calculation
        total = total + (t2 - t1) * 1000000

    # Average our time readings
    reading = total / 100

    # Convert our average time reading to a resistance
    resistance = reading * 6.05 - 939
    print(resistance)

try:
    resistance_reading()
except KeyboardInterrupt:
    print("\Quitting")

finally:
    GPIO.cleanup()