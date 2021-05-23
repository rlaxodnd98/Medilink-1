"""
Editor : Kim Jihwan, Kim Taeung
"""
from flask import Flask, url_for,render_template, redirect
from markupsafe import escape

import RPi.GPIO as GPIO
import time

from board import SCL, SDA
import busio

from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import sys

print(sys.version)

"""
Initial Setup
"""
app = Flask(__name__)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)   # LED control pin

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50
servo1 = servo.Servo(pca.channels[1])
time.sleep(0.05)
servo2 = servo.Servo(pca.channels[3])
time.sleep(0.05)
servo3 = servo.Servo(pca.channels[5], min_pulse=100, max_pulse=2600)
time.sleep(0.05)
#servo4 = servo.Servo(pca.channels[4])
#time.sleep(0.05)
relay = pca.channels[15]
servo5 = servo.Servo(pca.channels[8])
time.sleep(0.05)
servo6 = servo.Servo(pca.channels[10])
time.sleep(0.05)
servo7 = servo.Servo(pca.channels[12], min_pulse=100, max_pulse=2600)
time.sleep(0.05)

"""
initial angle
"""
servo1.angle = 80 # originally 40
servo2.angle = 120
time.sleep(0.05)
servo3.angle = 60
time.sleep(0.05)
#servo4.angle = 90
#time.sleep(0.05)
servo5.angle = 90
time.sleep(0.05)
servo6.angle = 120
time.sleep(0.05)
servo7.angle = 70
time.sleep(0.05)
#GPIO.output(12, GPIO.HIGH)
"""
APP.ROUTE
"""
class S(object):
    _instance = None
    led_on = False
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


def leftarm_move_left_right(x):
    angle3 = servo3.angle + x
    if angle3 < 90 and angle3 > 35:
        servo3.angle = angle3
        time.sleep(0.01)

def rightarm_move_left_right(x):
    angle7 = servo7.angle + x
    if angle7 < 150 and angle7 > 0:
        servo7.angle = angle7
        time.sleep(0.01)

def leftarm_move_up_down(y):
    angle1 = servo1.angle + y
    angle2 = servo2.angle + y
    if angle1 < 140 and angle1 > 30:
        servo1.angle = angle1
    if angle2 < 145 and angle2 > 35:
        servo2.angle = angle2
    time.sleep(0.01)

def rightarm_move_up_down(y):
    if servo5.angle > 60:
        angle5 = servo5.angle - y
        angle6 = servo6.angle - y
    else :
        angle5 = servo5.angle - 1.5 * y
        angle6 = servo6.angle - y
    if angle5 < 95 and angle5 > 5:
        servo5.angle = angle5
    if angle6 < 125 and angle6 > 55:
        servo6.angle = angle6
    time.sleep(0.01)
    
@app.route('/')
def render_webapp_page():
    return render_template('webapp.html')

# Right Arm
@app.route('/move/leftarm/<direction>', methods = ['POST'])
def leftarm_move_to_dir(direction):
    if direction == 'up':
        leftarm_move_up_down(5)
    elif direction == 'down':
        leftarm_move_up_down(-5)
    elif direction == 'right':
        leftarm_move_left_right(5)
    elif direction == 'left':
        leftarm_move_left_right(-5)
    else:
        return
    return render_template('move.html')

# Left Arm
@app.route('/move/rightarm/<direction>', methods = ['POST'])
def rightarm_move_to_dir(direction):
    if direction == 'up':
        rightarm_move_up_down(5)
    elif direction == 'down':
        rightarm_move_up_down(-5)
    elif direction == 'right':
        rightarm_move_left_right(-5)
    elif direction == 'left':
        rightarm_move_left_right(5)
    return render_template('move.html') 

# Medical Light
@app.route('/light/', methods = ['POST'])
def light_on():
    if S.led_on == False:
        GPIO.output(18, GPIO.HIGH)
        S.led_on = True
    else:
        GPIO.output(18, GPIO.LOW)
        S.led_on = False
    return render_template('move.html')
