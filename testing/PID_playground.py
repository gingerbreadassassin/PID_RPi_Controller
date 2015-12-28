from math import fabs

def measure(control, reading): # will take reading from sensor later
    return reading - control*0.01

def calc_err(target, measured_value):
    return measured_value - target

def differential(err1, err2, delta):
    return (err1 - err2)/delta

def outputcalc(kp, ki, kd, error, integral, diffntl):
    error *= kp
    integral *= ki
    diffntl *= kd
    return error + integral + diffntl

def main():
    err1 = 0
    print("Welcome to the PID simpulator.")
    setpoint = float(input("Enter a desired temperature: "))
    measurement = float(input("Enter an initial measurement: "))
    delta = float(input("Enter a delta T (change in time between samples): "))
    kp = float(input("Enter proportional gain: "))
    ki = float(input("Enter integral gain: "))
    kd = float(input("Enter differential gain: "))
    interval = 0.0
    err2 = calc_err(setpoint, measurement)
    integral = err1*delta
    diffntl = differential(err1, err2, delta)
    err1 = err2
    output = outputcalc(kp, ki, kd, err1, integral, diffntl)

    while fabs(err2) > 0.000001:
        interval += delta
        measurement = measure(output, measurement)
        err2 = calc_err(setpoint, measurement)
        integral += err1*delta
        diffntl = differential(err1, err2, delta)
        output = outputcalc(kp, ki, kd, err1, integral, diffntl)
        err1 = err2

    print("It took " + str(interval) + " seconds to stabilize.")

try:
    main()

except KeyboardInterrupt:
    pass