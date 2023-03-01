import time
import board
import digitalio
from adafruit_motor import stepper
import sys

#Based on examples from  SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries



class StepperControl(object):
    def __init__(self):
        self.DELAY = 0.005
        self.STEPS = 400
        self.currPos = 0
        self.coils = (
            digitalio.DigitalInOut(board.D19),  # A1
            digitalio.DigitalInOut(board.D26),  # A2
            digitalio.DigitalInOut(board.D20),  # B1
            digitalio.DigitalInOut(board.D21),  # B2
        )
        for coil in self.coils:
            coil.direction = digitalio.Direction.OUTPUT
        self.motor = stepper.StepperMotor(self.coils[0], self.coils[1], self.coils[2], self.coils[3], microsteps=None)
    def move(self, degrees, mydirection): #tragically right now degrees is just steps. It's very close to the 400
        print("moving")
        #stepper.BACKWARD
        if mydirection < 0:
            for step in range(degrees):
                self.motor.onestep(direction=stepper.BACKWARD)
                time.sleep(self.DELAY)
        else:
            for step in range(degrees):
                self.motor.onestep()
                time.sleep(self.DELAY)
            

