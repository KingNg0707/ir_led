# -*- coding: utf-8 -*-
from ioctrl import GpioCtrl


class Processes(object):
    flag_ir_send_act=False

    def __init__(self):
        self.Gpio_Ctrl=GpioCtrl()

    def IR_Send(self):
        pass
