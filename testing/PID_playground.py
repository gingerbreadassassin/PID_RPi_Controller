
def measure(control, reading): # will take reading from sensor later
    print("Running measurement function...")
    print(reading - control*0.01)
    return reading - control*0.01

def calc_err(target, measured_value):
    print("Running error calculation function...")
    print(measured_value - target)
    return measured_value - target

def differential(err1, err2, delta):
    print("Running differential function...")
    print((err2 - err1)/delta)
    return (err2 - err1)/delta

def outputcalc(kp, ki, kd, error, integral, diffntl):
    print("Running output calculator function...")
    error *= kp
    print("error: ", error)
    integral *= ki
    print("integral: ", integral)
    diffntl *= kd
    print("differential: ", diffntl)
    print("sum: ", error + integral + diffntl)
    return error + integral + diffntl

def main():
    print("Trying main function...")
    print("Welcome to the PID simpulator.")
    setpoint = 75.0 # float(input("Enter a desired temperature: "))
    measurement = 62.0 # float(input("Enter an initial measurement: "))
    print("measurement: ", measurement)
    delta = 0.1 # float(input("Enter a delta T (change in time between samples): "))
    kp = 1.0 # float(input("Enter proportional gain: "))
    ki = 1.0 # float(input("Enter integral gain: "))
    kd = 1.0 # float(input("Enter differential gain: "))
    interval = 0.0
    err1 = calc_err(setpoint, measurement)
    print("err1: ", err1)
    # integral = integrate(calc_err, 0.0, interval)[0]
    integral = 0
    diffntl = differential(err1, 0, delta)
    print("differential: ", diffntl)
    output = outputcalc(kp, ki, kd, err1, integral, diffntl)

    print("The initial state:")
    print("Proportional component: " + str(kp*err1))
    print("Integral component:     " + str(ki*integral))
    print("Differential component: " + str(kd*diffntl))
    print("Control output:         " + str(output))

    while input("Press Enter to continue...") is None:
        interval += delta
        print("interval: ", interval)
        measurement = measure(output, measurement)
        print("measurement: ", measurement)
        err2 = calc_err(setpoint, measurement)
        print("err2: ", err2)
        if err2 < 0.000001:
            err2 = 0
        integral += err1*delta
        print("integral: ", integral)
        if integral < 0.000001:
            integral = 0
        diffntl = differential(err1, err2, delta)
        print("differential: ", diffntl)
        if diffntl < 0.000001:
            diffntl = 0
        output = outputcalc(kp, ki, kd, err1, integral, diffntl)
        err1 = err2
        print("err1: ", err1)

        print("State after " + str(interval) +" seconds:")
        print("Temperature: " + str(measurement))
        print("Proportional component: " + str(kp*err1))
        print("Integral component:     " + str(ki*integral))
        print("Differential component: " + str(kd*diffntl))
        print("Control output:         " + str(output))

    print("It took " + str(interval) + " seconds to stabilize.")

try:
    main()

except KeyboardInterrupt:
    pass