import logging
import threading
import time
import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from ioctrl import GpioCtrl


class Processes(threading.Thread):
    flag_ir_send_act = False
    ALIVE_NOTIFY_JOB_ID = "main_schedule"

    def __init__(self, config):
        super().__init__(daemon=True)
        self.logger = logging.getLogger(__name__)
        self.config = config

        self._gpio = GpioCtrl()

        self._scheduler = BackgroundScheduler()
        self._scheduler.add_job(self.IR_Send,
                                trigger="interval",
                                name=Processes.ALIVE_NOTIFY_JOB_ID,
                                id=Processes.ALIVE_NOTIFY_JOB_ID,
                                minutes=config.Time.time_main_schedule)

        self.restart_event = threading.Event()

    def run(self):
        self._gpio.start()
        self._scheduler.start()

    def shutdown(self):
        if self._scheduler.running:
            self._scheduler.shutdown(wait=True)

        self._gpio.stop()

    def IR_Send(self):
        logging.info("To send")
        cmd = self._gpio.ir_cmd
        if cmd:
            output = True
            for i in cmd:
                self._gpio.output(self._gpio._OUTPUT_IR_LED, output)
                time.sleep(cmd[i])
                output = not output

        self._gpio.ir_cmd = []
