import logging
import sys
import threading

from processes import Processes

myprocesses = Processes()


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger = logging.getLogger("IR")

    # proc_ir_send = threading.Thread(target=myprocesses.IR_Send)

    while True:

    #
    #     if myprocesses.flag_ir_send_act is False:
    #         myprocesses.flag_ir_send_act = True
    #     try:
    #         if myprocesses.flag_ir_send_act is True:
    #             #
    #             if proc_ir_send.is_alive() is False:
    #                 print("#A1# ")
    #                 proc_ir_send.start()
    #                 print("#A2# : ", proc_ir_send.is_alive())
    #     except:
    #         logger.info(f"Unexpected error:{sys.exc_info()}")
    #         break  # just for test
    #
    # else:
    #     myprocesses.flag_ir_send_act = False


if __name__ == "__main__":
    try:
        main()
    finally:
        myprocesses.shutdown()
