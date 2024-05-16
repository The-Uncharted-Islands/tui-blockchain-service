import deposit.deposit_event as deposit_event
from util.logger import logger
import time
import util.signal_handler as signal_handler


logger.info("doposit server start...")
signal_handler.init()
deposit_event.load_config()
while signal_handler.is_running():
    deposit_event._once_scan()
    time.sleep(12)
