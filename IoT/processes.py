# -*- coding: utf-8 -*-
from code.ioctrl import GpioCtrl
import threading

class Processes(threading.Thread):
    flag_ir_send_act = False

    def __init__(self):
        self.Gpio_Ctrl = GpioCtrl()

    def IR_Send(self):
        pass

    def shutdown(self):
        self.Gpio_Ctrl.stop()

