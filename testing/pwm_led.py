import pigpio

pi = pigpio.pi()

def pwm_percent():
        pwmpercent = input("Enter PWM duty cycle percent of 0-100 (CTRL+C to exit): ")
        if 0 > pwmpercent > 100:
            print("Sorry, try again.")
            pwm_percent()
        return pwmpercent * 10000

def pwm_freq():
    freq = int(input("Enter frequency in Hz >= 1: "))
    if freq < 1:
        print("Sorry, try again.")
        pwm_freq()
    return freq

def main(fq, dc):
    print("1. Change frequency")
    print("2. Change duty cycle")
    print("3. Execute")
    print("4. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        fq = pwm_freq()
    if choice == 2:
        dc = pwm_percent()
    if choice == 3:
        pi.hardware_PWM(18, fq, dc)
    if choice == 4:
        pi.write(18, 0)
        pi.stop()
        exit()
    else:
        print("Please choose an option from the menu.")
        main(fq, dc)

try:
    print("Welcome to PWM LED testing!")
    while True:
        fq = pwm_freq()
        dc = pwm_percent()
        main(fq, dc)
except UnboundLocalError:
    print("Please choose an option from the menu.")
    main(fq, dc)
except KeyboardInterrupt:
    print
    pass
pi.write(18, 0)
pi.stop()
