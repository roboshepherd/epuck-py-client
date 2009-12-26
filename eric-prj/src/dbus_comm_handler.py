import time, os, sys, sched, subprocess, re, signal, traceback
import gobject, dbus, dbus.service, dbus.mainloop.glib 
import multiprocessing,  logging
from RILSetup import DBUS_IFACE,  DBUS_PATH
from data_manager import *

#datamgr_proxy = DataManager()
iter = 0

def save_pose(key,  pose_val):
    global datamgr_proxy
    try:
        datamgr_proxy.mRobotPose[key] = pose_val
        print datamgr_proxy.mRobotPose
    except:
       print "Err"
       sys.exit(0) 

def robot_signal_handler( sig,  val):
    global iter
    print "Caught signal  %s (in robot signal handler) %d "  %(sig,  val)
    iter = iter+1
    save_pose(iter,  val)
 

def main_loop():
    try:
        loop = gobject.MainLoop()
        loop.run()
    except (KeyboardInterrupt, SystemExit):
        print "User requested exit... shutting down now"
        pass
        sys.exit(0)

def client_main(data_mgr,  dbus_iface= DBUS_IFACE,  dbus_path = DBUS_PATH,  sig = "RobotPose"):
        global datamgr_proxy
        datamgr_proxy = data_mgr
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        try:
            bus.add_signal_receiver(robot_signal_handler, dbus_interface = DBUS_IFACE, signal_name = sig)
            main_loop()
        except dbus.DBusException:
            traceback.print_exc()
            sys.exit(1)
