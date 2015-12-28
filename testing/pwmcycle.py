import time, pigpio

pi = pigpio.pi()

try:
    while 1:
        for dc in range(0, 101, 1):
            pi.hardware_PWM(19, 25000, dc*10000)
            time.sleep(0.1)
        for dc in range(100 , -1, -1):
            pi.hardware_PWM(19, 25000, dc*10000)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
pi.write(19, 0)
pi.stop()
