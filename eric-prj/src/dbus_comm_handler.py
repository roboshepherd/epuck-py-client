import time, os, sys, sched, subprocess, re, signal, traceback
import gobject, dbus, dbus.service, dbus.mainloop.glib 
import multiprocessing,  logging,  logging.config,  logging.handlers
logging.config.fileConfig("logging.conf")
logger = logging.getLogger("EpcLogger")
from RILSetup import *
from data_manager import *

#--------------------- Signal Reception ----------------------------
def extract_objects(object_list):
	list = []
	for object in object_list:
		val = str(object)
		list.append(eval(val) )
	return  list

def save_pose(pose):
    global datamgr_proxy
    try:
        datamgr_proxy.mRobotPose.clear()
        for k, v in pose.iteritems():
            key = str(k)
            value = eval(str(v))
            datamgr_proxy.mRobotPose[key] = value 
        datamgr_proxy.mRobotPoseAvailable.set()
        print datamgr_proxy.mRobotPose
        #logger.info("RobotPose-x %f",  datamgr_proxy.mRobotPose[1])
        logger.info("@DBC RobotPose recvd. len logged: %d" ,\
            len(datamgr_proxy.mRobotPose))
    except:
       print "Err in save_pose()"

def save_taskinfo(taskinfo):
    global datamgr_proxy
    try:
        datamgr_proxy.mTaskInfo.clear()
        for k, v in taskinfo.iteritems():
            key = eval(str(k))
            value = extract_objects(v)
            datamgr_proxy.mTaskInfo[key] = value 
        datamgr_proxy.mTaskInfoAvailable.set()
        print datamgr_proxy.mTaskInfo
    except:
       print "Err in save_taskinfo()"

def pose_signal_handler( sig,  val):
    print "Caught signal  %s (in pose signal handler) "  %(sig)
    #print "Val: ",  val
    save_pose( val)
 
def taskinfo_signal_handler( sig,  val):
    print "Caught signal  %s (in taskinfo signal handler) "  %(sig)
    #print "Val: ",  val
    save_taskinfo(val)
 
def main_loop():
    try:
        loop = gobject.MainLoop()
        loop.run()
    except (KeyboardInterrupt, SystemExit):
        print "User requested exit... shutting down now"
        pass
        sys.exit(0)

def client_main(data_mgr,  dbus_if1= DBUS_IFACE_TRACKER,\
            dbus_path1 = DBUS_PATH_BASE,\
            dbus_if2= DBUS_IFACE_TASK_SERVER, \
            dbus_path2 = DBUS_PATH_TASK_SERVER,\
            sig1 = SIG_ROBOT_POSE, sig2 = SIG_TASK_INFO,  delay=3 ):
        global datamgr_proxy,  task_signal
        datamgr_proxy = data_mgr
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        try:
            bus.add_signal_receiver(pose_signal_handler, dbus_interface =\
                                     dbus_if1, path= dbus_path1,  signal_name = sig1)
            bus.add_signal_receiver(taskinfo_signal_handler, dbus_interface =\
                                     dbus_if2, path= dbus_path2,  signal_name = sig2)
            main_loop()
        except dbus.DBusException:
            traceback.print_exc()
            sys.exit(1)
