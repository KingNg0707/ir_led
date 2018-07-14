import logging
import sys

from processes import Processes


def main():
    import config as config
    import time_utils

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger = logging.getLogger("IR")

    # proc_ir_send = threading.Thread(target=myprocesses.IR_Send)

    while True:
        myprocesses = Processes(config)

        logger.info(f"Start: {config.Time.time_start}")
        logger.info(f"Stop: {config.Time.time_end}")
        logger.info(f"Now: {time_utils.get_datetime_now().timetz().isoformat()}")

        try:
            myprocesses.start()
            myprocesses.restart_event.wait()
            myprocesses.join()

        except KeyboardInterrupt:
            sys.exit(1)

        except Exception as ex:
            logger.exception(ex)

        finally:
            myprocesses.shutdown()

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
    main()
