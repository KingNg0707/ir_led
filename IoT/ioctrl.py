import logging
from datetime import datetime as datetime

from RPi import GPIO


class GpioCtrl(object):
    _CHANNEL = 18
    _OUTPUT_IR_LED = 32

    def __init__(self):
        logging.info("#B1# gpio init")

    def start(self):
        logging.info("#B2# gpio start")
        GPIO.setmode(GPIO.BOARD)

        # input
        GPIO.setup(self._CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self._CHANNEL, edge=GPIO.BOTH, callback=self._receive_both_callback)

        # output
        GPIO.setup(self._OUTPUT_IR_LED, GPIO.OUT)

    def stop(self):
        GPIO.remove_event_detect(self._CHANNEL)
        GPIO.cleanup()

    def _receive_both_callback(self, pin):
        GPIO.remove_event_detect(self._CHANNEL)

        logging.info(f"#B3# gpio callback from channel {pin}")
        i = 1000000
        last_state = False
        while i > 0:
            state = self._get_state(self._CHANNEL)
            if last_state != state:
                time=datetime.now()
                logging.info(f"changed: {time}\t0")
                logging.info(f"changed: {time}\t1")
            last_state = state

            i -= 1

        logging.info(f"callback end: {datetime.now()}")

    def _get_state(self, pin):
        try:
            return GPIO.input(pin)
        except:
            raise Exception("Not match CHANNEL")
