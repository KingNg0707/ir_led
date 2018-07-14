# -*- coding: utf-8 -*-
from RPi import GPIO


class GpioCtrl(object):
    _CHANNEL = 18
    _OUTPUT_IR_LED = 32

    def __init__(self):
        print("#B1# gpio init")
        GPIO.setup(self._OUTPUT_IR_LED, GPIO.OUT)

    def start(self):
        print("#B2# gpio start")
        GPIO.setmode(GPIO.BOARD)

        # input
        GPIO.setup(self._CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self._CHANNEL, edge=GPIO.FALLING, callback=self._receive_callback)

        # output
        GPIO.setup(self._OUTPUT_IR_LED, GPIO.OUT)

    def stop(self):
        GPIO.remove_event_detect(self._CHANNEL)
        GPIO.cleanup()

    def _receive_callback(self):
        print("#B3# gpio callback")

