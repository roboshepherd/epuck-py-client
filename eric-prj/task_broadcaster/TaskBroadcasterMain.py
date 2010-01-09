#!/usr/bin/python
import multiprocessing,  logging,  logging.config,  logging.handlers,  time
import sys
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
    # arg parsing
    numargs = len(sys.argv) - 1
    if numargs > 1 or numargs < 1:
        print "usage:" + sys.argv[0] + "<robot count >"
        sys.exit(1) 
    else:
        robots = int(sys.argv[1])
    # init stuff
    dm = DataManager()
    sig1 = SIG_TASK_INFO
    sig2 = SIG_TASK_STATUS
    delay = 2 # interval between signals
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
        args=(dm,  DBUS_IFACE_EPUCK, DBUS_PATH_BASE, robots,\
            sig2,   delay))
    main()   




