import sys
import logging
from datetime import datetime as datetime
import time

from RPi import GPIO

from ringbuffer import RingBuffer
import time_utils


class GpioCtrl(object):
    _INPUT_IR_RECEIVER = 18
    _INPUT_BUTTON = 22
    _OUTPUT_IR_LED = 32

    def __init__(self):
        logging.info("#B1# gpio init")
        self._rb = RingBuffer(500)
        self.ir_cmd = []

    def start(self):
        logging.info("#B2# gpio start")
        GPIO.setmode(GPIO.BOARD)

        # IR Receiver input
        GPIO.setup(self._INPUT_IR_RECEIVER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Button input
        GPIO.setup(self._INPUT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self._INPUT_BUTTON, edge=GPIO.FALLING, callback=self._receive_callback)

        # IR LED output
        GPIO.setup(self._OUTPUT_IR_LED, GPIO.OUT)
        GPIO.output(self._OUTPUT_IR_LED, 0)

    def stop(self):
        GPIO.remove_event_detect(self._INPUT_BUTTON)
        GPIO.cleanup()

    def _receive_callback(self, pin):
        GPIO.remove_event_detect(self._INPUT_BUTTON)

        logging.info(f"#B3# gpio callback from channel {pin}")
        self._rb = RingBuffer(1000)
        self._write_buffer(1000000)

        logging.info(f"callback end: {datetime.now()}")

        self._load_buffer()
        self.send_cmd(self.ir_cmd)

        GPIO.add_event_detect(self._INPUT_BUTTON, edge=GPIO.FALLING, callback=self._receive_callback)

    def _write_buffer(self, count):
        i = 0
        last_state = True
        while i < count:
            current_state = self._get_state(self._INPUT_IR_RECEIVER)
            if last_state != current_state:
                self._rb.add(datetime.now())
                # time = datetime.now()
                # logging.info(f"changed: {time}\t0")
                # logging.info(f"changed: {time}\t1")
                last_state = current_state
            i += 1

    def _load_buffer(self):
        count = 0
        first_time = self._rb.get()
        last_time = first_time
        delta_time = 0
        self.ir_cmd = []
        for i in range(self._rb.__len__()):
            try:
                current_time = self._rb.get()
                d = time_utils.str2float(f'{(current_time - last_time)}'.split(':', 2)[-1])
                self.ir_cmd.append(d)
                print(f"d:{d}")
                if d < 0.00055:
                    count += 1
                else:
                    print(f"count {count}")
                    dd = f'{(last_time - first_time)}'.split(':', 2)[-1]
                    print(f"dd:{dd}")
                    if dd != "00":
                        delta_time = time_utils.str2float(dd)
                    print(f"delta_time: {delta_time}")
                    if (delta_time != 0) and (count != 0):
                        f = 1 / (delta_time / count)
                        print(f"Frequency: {f}")
                    count = 0
                print((f'{current_time - first_time}'.split(':', 2)[-1]))
                last_time = current_time
                # print((f'{current_time}'))
            except:
                print(f"error:{sys.exc_info()}")
                break

    def _get_state(self, pin):
        try:
            return GPIO.input(pin)
        except:
            raise Exception("Not match CHANNEL")

    def output(self, pin, value):
        GPIO.output(pin, value)

    def pwm(self, pin, freq):
        return GPIO.PWM(pin, freq)

    def send_cmd(self, cmd):
        print(f"in send cmd {cmd}")
        pwm = self.pwm(self._OUTPUT_IR_LED, 37 * 1000)

        # first_state = False
        print("start")
        for j in range(100):
            pwm.ChangeFrequency(37 * 1000 + j * 400)
            # first_state = not first_state
            # self.output(self._OUTPUT_IR_LED, first_state)
            pwm.start(100)
            for i in range(len(cmd) - 1):
                if cmd[i] < 0.2:
                    pwm.ChangeDutyCycle(0)
                    time.sleep(cmd[i] - j * 0.000001)
                    i += 1
                    pwm.ChangeDutyCycle(100)
                    time.sleep(cmd[i] - j * 0.000001)

                    # self.output(self._OUTPUT_IR_LED, first_state)
                    # first_state = not first_state
            pwm.stop()
            self.output(self._OUTPUT_IR_LED, True)
            time.sleep(1)
            print(f"send completed {j}.")
