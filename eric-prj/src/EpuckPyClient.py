#!/usr/bin/python
import multiprocessing,  logging,  time
from RILSetup import *
from data_manager import *
from dbus_server import *
from dbus_comm_handler import *

multiprocessing.log_to_stderr(logging.DEBUG)

#def main():
#    print "--- Start test---"
#    time.sleep(10)
#    print "--- End test---"

def server_proc(dbus_iface,  dbus_path,  sig1, sig2,  delay):
    """Emits DBus signal RobotPose and TaskInfo """
    name = multiprocessing.current_process().name
    print name, 'Starting'
    server_main(dbus_iface,  dbus_path,  sig1, sig2,  delay)

def client_proc(data_mgr,  dbus_iface,  dbus_path,  sig1,  sig2):
    """Catches DBus signal RobotPose and TaskInfo  and saves into DataManager"""
    name = multiprocessing.current_process().name
    print name, 'Starting'
    client_main(data_mgr,  dbus_iface,  dbus_path,  sig1,  sig2)

if __name__ == '__main__':
     dm = DataManager()
     sig1 = "RobotPose"
     sig2 = "TaskInfo"
     delay = 3 # interval between signals
     dbus_server = multiprocessing.Process(target=server_proc,\
                                name="RIL_dbus_server",  args=(DBUS_IFACE, DBUS_PATH,  sig1, sig2,  delay,  ))
     dbus_client = multiprocessing.Process(target=client_proc,\
                                name="RIL_dbus_client",  args=(dm,  DBUS_IFACE, DBUS_PATH, sig1,  sig2 ))
     dbus_server.start()
     dbus_client.start()
     time.sleep(10)
     dbus_server.join()
     dbus_client.join()

