from math import fabs

def measure(control, reading): # will take reading from sensor later
    # print("Running measurement function...")
    # print(reading - control*0.01)
    return reading - control*0.01

def calc_err(target, measured_value):
    # print("Running error calculation function...")
    # print(measured_value - target)
    return measured_value - target

def differential(err1, err2, delta):
    # print("Running differential function...")
    # print((err1 - err2)/delta)
    return (err1 - err2)/delta

def outputcalc(kp, ki, kd, error, integral, diffntl):
    # print("Running output calculator function...")
    error *= kp
    # print("error: ", error)
    integral *= ki
    # print("integral: ", integral)
    diffntl *= kd
    # print("differential: ", diffntl)
    # print("sum: ", error + integral + diffntl)
    return error + integral + diffntl

def main():
    err1 = 0
    # print("Trying main function...")
    print("Welcome to the PID simpulator.")
    setpoint = float(input("Enter a desired temperature: "))
    measurement = float(input("Enter an initial measurement: "))
    # print("measurement: ", measurement)
    delta = float(input("Enter a delta T (change in time between samples): "))
    kp = float(input("Enter proportional gain: "))
    ki = float(input("Enter integral gain: "))
    kd = float(input("Enter differential gain: "))
    interval = 0.0
    err2 = calc_err(setpoint, measurement)
    # err1 = 0
    # print("err2: ", err1)
    # integral = integrate(calc_err, 0.0, interval)[0]
    integral = err1*delta
    diffntl = differential(err1, err2, delta)
    err1 = err2
    # print("differential: ", diffntl)
    output = outputcalc(kp, ki, kd, err1, integral, diffntl)

    print("The initial state:")
    # print("Proportional component: " + str(kp*err1))
    # print("Integral component:     " + str(ki*integral))
    # print("Differential component: " + str(kd*diffntl))
    print("Control output:         " + str(output))

    # chk = 1
    # while chk == 1:
    while fabs(err2) > 0.00001:
        # chk = input("Enter 1 to iterate...")
        interval += delta
        # print("interval: ", interval)
        measurement = measure(output, measurement)
        # print("measurement: ", measurement)
        err2 = calc_err(setpoint, measurement)
        # print("err2: ", err2)
        if fabs(err2) < 0.000001:
            err2 = 0
        integral += err1*delta
        # print("integral: ", integral)
        if fabs(integral) < 0.000001:
            integral = 0
        diffntl = differential(err1, err2, delta)
        # print("differential: ", diffntl)
        if fabs(diffntl) < 0.000001:
            diffntl = 0
        output = outputcalc(kp, ki, kd, err1, integral, diffntl)
        err1 = err2
        # print("err1: ", err1)

        # print("State after " + str(interval) +" seconds:")
        # print("Temperature: " + str(measurement))
        # print("Proportional component: " + str(kp*err1))
        # print("Integral component:     " + str(ki*integral))
        # print("Differential component: " + str(kd*diffntl))
        # print("Control output:         " + str(output))

    print("It took " + str(interval) + " seconds to stabilize.")

try:
    main()

except KeyboardInterrupt:
    pass