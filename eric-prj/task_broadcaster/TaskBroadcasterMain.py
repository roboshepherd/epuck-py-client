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
        updater .start()
        emitter.start()
        receiver.start()
        # Ending....
        time.sleep(10)
        updater.join()
        emitter.join()
        receiver.join()
        logging.debug("--- End EPC---")


if __name__ == '__main__':
     dm = DataManager()
     sig1 = SIG_TASK_INFO
     sig2 = SIG_TASK_STATUS
     delay = 1 # interval between signals
     updater = multiprocessing.Process(\
        target=taskinfo_updater. updater_main,\
        name="TaskInfoUpdater",  args=(dm, ))
     emitter= multiprocessing.Process(\
        target=taskinfo_emitter.emitter_main,\
        name="TaskInfoEmitter",\
        args=(dm,  DBUS_IFACE_TASK_SERVER,\
            DBUS_PATH_TASK_SERVER, sig1,   delay,  ))
     receiver = multiprocessing.Process(\
            target=robotstatus_receiver.receiver_main,\
            name="TaskStatusReceiver",\
            args=(dm,  DBUS_IFACE_EPUCK, DBUS_PATH_BASE,\
                sig2,   delay ))
     main()   
     
      


