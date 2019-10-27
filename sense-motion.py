import RPi.GPIO as GPIO
import time
import sys
import fileinput
from pygame import mixer
import random

GPIO.setmode(GPIO.BCM)
mixer.init()

TRIG = 12
ECHO = 23
SONG_PATHS = [
    "/home/pi/Documents/Cricut/jpark/jpark-motion-sensor/theme.wav",
    "/home/pi/Documents/Cricut/jpark/jpark-motion-sensor/welcome.wav",
    "/home/pi/Documents/Cricut/jpark/jpark-motion-sensor/life.wav",
    "/home/pi/Documents/Cricut/jpark/jpark-motion-sensor/raptor1.wav",
    "/home/pi/Documents/Cricut/jpark/jpark-motion-sensor/trex1.wav",
    "/home/pi/Documents/Cricut/jpark/jpark-motion-sensor/trex2.wav",
    "/home/pi/Documents/Cricut/jpark/jpark-motion-sensor/trex3.wav"
]

def setUpSensors():
    print("Distance measurment in Progress")
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    print("Waiting for sensor to settle.")

    time.sleep(2)

def motionDetected(inDistance):
    songNumber = random.randint(0, len(SONG_PATHS) - 1)
    print("Motion Detected! Distance:", inDistance, "cm")
    print("Starting sound")
    song = mixer.Sound(SONG_PATHS[songNumber])
    timeToSleep = song.get_length() + 5
    print("Stopping motion detection for", timeToSleep, "seconds")
    song.play()
    time.sleep(song.get_length() + 5)
    print("Starting motion detection")


def detectMotion():
    print("Starting motion detection")
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
            if distance < lowLimit or distance > highLimit:
                motionDetected(distance)
            time.sleep(.05)

print("Current Distance (in cm)?")
desiredDistance = int(input())
lowLimit = desiredDistance - 50;
highLimit = desiredDistance + 50;
setUpSensors()
detectMotion()
