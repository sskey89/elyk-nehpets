
# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time
from keyboard_fun import get
# Import the PCA9685 module.
import Adafruit_PCA9685

d = 200000
# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
def delay(num):
    n = 0
    while n < num:
        n = n+1
        pass
    pass

def test():
    pwm.set_pwm_freq(60)

    print('Moving servo on channel 0, press Ctrl-C to quit...')
    while True:
        # Move servo on channel O between extremes.
        pwm.set_pwm(0, 0, servo_min)
        pwm.set_pwm(1, 0, servo_min)
        time.sleep(1)
        pwm.set_pwm(0, 0, servo_max)
        pwm.set_pwm(1, 0, servo_max)
        time.sleep(1)
        pass

def characterize_servo(channel):
    pwm.set_pwm_freq(50)
    start = 130
    fin = 540
    middle = int((start + fin)/2)
    while start <= fin:
        print "Setting servo to position: %d" % start
        pwm.set_pwm(channel, 0, start)
        delay(d)
        start = start + 1
        pass
    pass
    pwm.set_pwm(channel, 0, middle)
    time.sleep(1)
       
def move_pt(pan_ch, tilt_ch):
    pwm.set_pwm_freq(50)
    pan_start = 130
    tilt_start = 160
    end = 540
    #pan_pos = int((pan_start + end)/2)
    #tilt_pos = int((tilt_start + end)/2)
    pan_pos = 344
    tilt_pos = 335
    pwm.set_pwm(pan_ch, 0, pan_pos)
    pwm.set_pwm(tilt_ch, 0, tilt_pos)
    while(True):
        k = get()
        if k == "left" and pan_pos < end:
           pan_pos += 1
           pass
	elif k == "right" and pan_pos > pan_start:
           pan_pos -= 1
	   pass
        elif k == "up" and tilt_pos < end:
	   tilt_pos += 1
           pass
	elif k == "down" and tilt_pos > tilt_start:
	   tilt_pos -= 1
           pass	
        if k !="":
           print "Pan Pos: %d, Tilt Pos: %d" % (pan_pos, tilt_pos)
           pass
        pwm.set_pwm(pan_ch, 0, pan_pos)
        pwm.set_pwm(tilt_ch, 0, tilt_pos)
	pass 
    
if __name__ == "__main__":
    #characterize_servo(0)
    move_pt(0,1)
	
