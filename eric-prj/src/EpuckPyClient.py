#!/usr/bin/python
import multiprocessing,  logging,  logging.config,  logging.handlers,  time

logging.config.fileConfig("logging.conf")
#create logger
logger = logging.getLogger("EpcLogger")

from RILSetup import *
from data_manager import *
from ril_robot import *
import dbus_server
import dbus_comm_handler 
import task_selector
multiprocessing.log_to_stderr(logging.DEBUG)

def main():
        logging.debug("--- Start EPC---")
        dbus_server.start()
        dbus_client.start()
        taskselector.start()
        # Ending....
        time.sleep(10)
        dbus_server.join()
        dbus_client.join()
        taskselector.join()
        logging.debug("--- End EPC---")


if __name__ == '__main__':
     dm = DataManager()
     robot = RILRobot(id=1)
     robot.InitTaskRecords(MAXSHOPTASK)
     sig1 = "RobotPose"
     sig2 = "TaskInfo"
     delay = 3 # interval between signals
     dbus_server = multiprocessing.Process(target=dbus_server.server_main,\
                                name="RIL_dbus_server",  args=(DBUS_IFACE, DBUS_PATH,  sig1, sig2,  delay,  ))
     dbus_client = multiprocessing.Process(target=dbus_comm_handler.client_main,\
                                name="RIL_dbus_client",  args=(dm,  DBUS_IFACE, DBUS_PATH, sig1,  sig2 ))
     taskselector = multiprocessing.Process(target=task_selector.selector_main,\
                                name="TaskSelector",  args=(dm,  robot ))
                                                                     
     main()
      


