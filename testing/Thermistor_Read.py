# Adopted to pigpio from Ken Powers' work

import time, math, pigpio

pi = pigpio.pi()

def resistance_reading():
    total = 0
    for i in range(1, 100):
        # Discharge 330nF cap
        pi.set_mode(23, pigpio.INPUT)
        pi.set_mode(24, pigpio.OUTPUT)
        pi.write(24, 0)
        time.sleep(0.01)
        # Charge cap until GPIO reads HIGH
        pi.set_mode(24, pigpio.INPUT)
        pi.set_mode(23, pigpio.OUTPUT)
        pi.write(23, 1)
        t1 = time.time()
        while not pi.read(24):              # while pin reads nothing:
            pass                            #   do nothing
        t2 = time.time()
        # Record time interval and sum
        total += (t2-t1)*1000000
    # Average time readings
    reading = total / 100
    # Convert average time reading to resistance
    resistance = reading * 6.05 - 1739 # Use a multimeter to adjust this second value
    return resistance

def temperature_reading(r):
    b = 3435.0 # beta value from NTC Thermistor TTF3A103_34D
    r0 = 10000 # 10 KiloOhms @ 25deg Celsius
    t0 = 273.15 # degrees Kelvin at 0deg C
    t25 = t0 + 25.0 # 25deg C in K
    # Steinhart-Hart equation
    inv_t = 1/t25 + 1/b * math.log(r/r0)
    t = (1/inv_t - t0) * 1.0 # Adjustment value
    return t * 9.0 / 5.0 + 32.0 # Conversion C to F

try:
    print(temperature_reading(resistance_reading()))

except KeyboardInterrupt:
    pi.set_mode(23, 0)
    pi.set_mode(24, 0)
    pi.stop()
    pass