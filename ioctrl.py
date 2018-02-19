# -*- coding: utf-8 -*-
from RPi import GPIO

class GpioCtrl(object):
    CHANNEL = 18
    OUTPUT_IR_LED = 32
    def __init__(self):
        print("#B1# gpio init")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.OUTPUT_IR_LED, GPIO.OUT)