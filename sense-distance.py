import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)

TRIG = 12
ECHO = 23
loopcount = 0

print("Distance measurment in Progress")
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print("Waiting for sensor to settle.")

time.sleep(2)

while True:
	GPIO.output(TRIG, True)
  	time.sleep(0.00001)
  	GPIO.output(TRIG, False)
	pulse_start = time.time()
	while GPIO.input(ECHO)==0:
		pulse_start = time.time()
	while GPIO.input(ECHO)==1:
		pulse_end = time.time()
	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration*17150
	distance = round(distance, 2)
	print("Measured Distance:", distance, "cm")
	loopcount += 1
	time.sleep(.25)
	if loopcount > 20:
		GPIO.cleanup()
		sys.exit()      
