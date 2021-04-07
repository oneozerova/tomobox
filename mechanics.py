import time
from picamera import PiCamera
import RPi.GPIO as GPIO
from gpiozero  import LED
from time import sleep

GPIO.setmode(GPIO.BCM)

camera = PiCamera()
camera.resolution = (640,640)

camera.start_preview()
camera.start_recording('/home/pi/Desktop/video3.h264')

led1 = LED(25)
led2 = LED(24)

led1.on()
led2.on()

ControlPin = [7, 11, 13, 15]

for pin in ControlPin:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

seq = [ [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 1]
    ]

for i in range(512):
    for halfstep in range(8):
        for pin in range(4):
            GPIO.output(ControlPin[pin], seq[halfstep][pin])
        time.sleep(0.001)

GPIO.cleanup()

camera.stop_recording()
camera.stop_preview()


