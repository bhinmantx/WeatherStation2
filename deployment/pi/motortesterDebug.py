# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Use this example for digital pin control of an H-bridge driver
# like a DRV8833, TB6612 or L298N.

import time
import board
import digitalio
from adafruit_motor import stepper
import sys






STEPS = int(sys.argv[1])
DELAY = float(sys.argv[2])
COUNT = int(sys.argv[3])
#DELAY = 0.01
#STEPS = 400

# You can use any available GPIO pin on both a microcontroller and a Raspberry Pi.
# The following pins are simply a suggestion. If you use different pins, update
# the following code to use your chosen pins.


# To use with a Raspberry Pi:
coils = (
     digitalio.DigitalInOut(board.D19),  # A1
     digitalio.DigitalInOut(board.D26),  # A2
     digitalio.DigitalInOut(board.D20),  # B1
     digitalio.DigitalInOut(board.D21),  # B2
 )

for coil in coils:
    coil.direction = digitalio.Direction.OUTPUT

motor = stepper.StepperMotor(coils[0], coils[1], coils[2], coils[3], microsteps=None)



i = COUNT
while i > 0:
    for step in range(STEPS):
        motor.onestep()
        time.sleep(DELAY)
#print("36")
#    for step in range(STEPS):
#        motor.onestep(direction=stepper.BACKWARD)
#        time.sleep(DELAY)
   
    print(i)
    i = i - 1 
#    for step in range(STEPS):
#        motor.onestep(style=stepper.DOUBLE)
#        time.sleep(DELAY)
    '''
    print("44")
    for step in range(STEPS):
        motor.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        time.sleep(DELAY)
    
    print("48")
    for step in range(STEPS):
        motor.onestep(style=stepper.INTERLEAVE)
        time.sleep(DELAY)
    print("52")
    for step in range(STEPS):
        motor.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
        time.sleep(DELAY)
    print("56")
    '''
    '''DELAY = DELAY + .02
    print("delay is now " + str(DELAY))'''
motor.release()
