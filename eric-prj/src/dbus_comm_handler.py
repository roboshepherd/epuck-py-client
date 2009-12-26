import time, os, sys, sched, subprocess, re, signal, traceback
import gobject, dbus, dbus.service, dbus.mainloop.glib 
import multiprocessing,  logging

#from dbus.introspect_parser import process_introspection_data

from RILSetup import DBUS_IFACE,  DBUS_PATH
from data_manager import *

#def extract_objects(object_list):
#	list = "["
#	for object in object_list:
#		val = str(object)
#		list = list + val + " , "
#	list = list + "]"
#	return list

def extract_objects(object_list):
	list = []
	for object in object_list:
		val = str(object)
		list.append(eval(val) )
	return  list


def save_pose(pose_val):
    global datamgr_proxy
    try:
        datamgr_proxy.mRobotPose = []
        datamgr_proxy.mRobotPose = extract_objects(pose_val)
        print datamgr_proxy.mRobotPose
        print "Len:" ,  len(datamgr_proxy.mRobotPose)
    except:
       print "Err in save_pose()"

def save_taskinfo(key,  taskinfo):
    global datamgr_proxy
    try:
        datamgr_proxy.mTaskInfo.clear()
        datamgr_proxy.mTaskInfo = taskinfo.copy()
        #print datamgr_proxy.mTaskInfo
    except:
       print "Err in save_taskinfo()"

def pose_signal_handler( sig,  val):
    print "Caught signal  %s (in pose signal handler) "  %(sig)
    #print "Val: ",  val
    save_pose( val)
 
def taskinfo_signal_handler( sig,  val):
    print "Caught signal  %s (in taskinfo signal handler) "  %(sig)
    #print "Val: ",  val
    save_taskinfo(iter,  val)
 

def main_loop():
    try:
        loop = gobject.MainLoop()
        loop.run()
    except (KeyboardInterrupt, SystemExit):
        print "User requested exit... shutting down now"
        pass
        sys.exit(0)

def client_main(data_mgr,  dbus_iface= DBUS_IFACE,  dbus_path = DBUS_PATH,\
                sig1 = "RobotPose",  sig2 = "TaskInfo" ):
        global datamgr_proxy
        datamgr_proxy = data_mgr
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        try:
            bus.add_signal_receiver(pose_signal_handler, dbus_interface = DBUS_IFACE, signal_name = sig1)
            bus.add_signal_receiver(taskinfo_signal_handler, dbus_interface = DBUS_IFACE, signal_name = sig2)
            main_loop()
        except dbus.DBusException:
            traceback.print_exc()
            sys.exit(1)
