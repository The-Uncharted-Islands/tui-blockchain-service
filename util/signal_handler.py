import signal
import logging


LOOP_RUN = True


def proc_sign(a, b):
    global LOOP_RUN
    LOOP_RUN = False
    logging.info("user interrupt")


def init():
    logging.info("signal_handler init")
    signal.signal(signal.SIGINT, proc_sign)
    signal.signal(signal.SIGTERM, proc_sign)


def interrupt():
    global LOOP_RUN
    LOOP_RUN = False


def is_interrupt():
    return not LOOP_RUN


def is_running():
    return LOOP_RUN
