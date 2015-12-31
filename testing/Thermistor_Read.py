# Adopted to pigpio from Ken Powers' work

import time, math, pigpio

pi = pigpio.pi()

def resistance_calc(us, nf): # microsecond, nanoFarads
    t = us*1e-6
    c = nf*1e-9
    v = 1 - ((22.0/15.0)/3.3) # gpio high trigger voltage / supply voltage
    lnv = math.log1p(v-1) # log1p is natural log (1+x)
    return -t / (c * lnv)

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
        # t1 = time.time()
        t1 = pi.get_current_tick()
        while not pi.read(24):              # while pin reads nothing:
            pass                            #   do nothing
        # t2 = time.time()
        t2 = pi.get_current_tick()
        # Record time interval in microseconds and sum
        total += pigpio.tickDiff(t1, t2)
    # Average time readings
    reading = total / 100
    # Convert average time reading to resistance
    # print(resistance_calc(reading, 330))
    return resistance_calc(reading, 330) # pass average time, capacitance in nanoFarads

def temperature_reading(r):
    lr = math.log1p(r-1)
    # Steinhart-Hart equation using coefficients from bitspower thermistor probe
    tk = 1 / (0.000428670876749269 + 0.000322025554873117 * lr + -4.959174377042198e-8 * lr * lr * lr)
    tc = tk - 273.15 # Conversion K to C
    tf = tc * 9.0 / 5.0 + 32.0 # Conversion C to F
    return tk, tc, tf

def kelvin():
    return temperature_reading(resistance_reading())[0]

def celsius():
    return temperature_reading(resistance_reading())[1]

def fahrenheit():
    return temperature_reading(resistance_reading())[2]
