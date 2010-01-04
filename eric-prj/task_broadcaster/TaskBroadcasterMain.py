#!/usr/bin/python
import multiprocessing,  logging,  logging.config,  logging.handlers,  time

logging.config.fileConfig("logging.conf")
#create logger
logger = logging.getLogger("EpcLogger")
multiprocessing.log_to_stderr(logging.DEBUG)

from RILSetup import *
from data_manager import *
import taskinfo_emitter
import robotstatus_receiver
import taskinfo_updater

def main():
        logging.debug("--- Start EPC---")
        emitter.start()
        receiver.start()
        updater .start()
        # Ending....
        time.sleep(10)
        emitter.join()
        receiver.join()
        updater.join()
        logging.debug("--- End EPC---")


if __name__ == '__main__':
     dm = DataManager()
     sig1 = "TaskInfo"
     sig2 = "RobotStatus"
     delay = 3 # interval between signals
     emitter= multiprocessing.Process(target=taskinfo_emitter.emitter_main,\
                                name="RIL_dbus_server",  args=(DBUS_IFACE, DBUS_PATH,  sig1,   delay,  ))
     receiver = multiprocessing.Process(target=robotstatus_receiver.receiver_main,\
                                name="RIL_dbus_client",  args=(dm,  DBUS_IFACE, DBUS_PATH, sig1,   delay ))
     updater = multiprocessing.Process(target=taskinfo_updater.updater_main,\
                                name="TaskInfoUpdater",  args=(dm, ))
                                                                        
     main()
      


