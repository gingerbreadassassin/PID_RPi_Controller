import pigpio

pi = pigpio.pi()

try:
    while 1:
        pwmpercent = input("Enter PWM speed percent of 100 (CTRL+C to exit): ")
        if 0 > pwmpercent > 100:
            pwmpercent = input("Enter PWM speed percent of 100 (CTRL+C to exit): ")
        pwmpercent *= 10000
        pi.hardware_PWM(19, 25000, pwmpercent)
except KeyboardInterrupt:
    print
    pass
pi.write(19, 0)
pi.stop()
