#!/usr/bin/env python
import time, os, sys, sched, subprocess, re, signal, traceback
import gobject, dbus, dbus.service, dbus.mainloop.glib 
import multiprocessing,  logging
from RILSetup import DBUS_IFACE,  DBUS_PATH
from task_info import *
from pose import *

schedule = sched.scheduler(time.time, time.sleep)
pose = Pose(x=300,  y=200,  theta=2.5).info
ti = TaskInfo()
task0 = ShopTask(id =0,  x=900,  y=1000)
task1 = ShopTask(id=1,  x=100,  y=100)
task2 = ShopTask(id=2,  x=1500,  y=1200)
ti.AddTaskInfo(0,  task0.Info())
ti.AddTaskInfo(1,  task1.Info()) 
ti.AddTaskInfo(2,  task2.Info())
taskinfo = ti.all

class TrackerSignal(dbus.service.Object):
    def __init__(self, object_path):
        dbus.service.Object.__init__(self, dbus.SessionBus(), object_path)
        #global taskinfo
    @dbus.service.signal(dbus_interface= DBUS_IFACE, signature='sad')
    def RobotPose(self, sig,  pose):
        # The signal is emitted when this method exits
        #pass
        print "Tracker signal: %s" %sig
        print pose
    @dbus.service.signal(dbus_interface= DBUS_IFACE, signature='sa{iad}')
    def TaskInfo(self, sig,  taskinfo):
        # The signal is emitted when this method exits
        print "Tracker signal: %s  " % (sig)
        print taskinfo
    def Exit(self):
        loop.quit()

#Emit DBus-Signal
def emit_tracker_signal(sig1, sig2,   inc):
    print "At emit_tracker_signal():"
    #taskinfo.Print()
    global tracker_signal,  pose,  taskinfo
    schedule.enter(inc, 0, emit_tracker_signal, (sig1, sig2,   inc)) # re-schedule to repeat this function
    print "\tEmitting signal>>> " 
    tracker_signal.RobotPose(sig1,  pose)
    tracker_signal.TaskInfo(sig2,  taskinfo)


def server_main(dbus_iface= DBUS_IFACE,  dbus_path = DBUS_PATH, \
                sig1 = "RobotPose", sig2= "TaskInfo",  delay = 1):
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    global tracker_signal,  taskinfo
    try:
        name = dbus.service.BusName(dbus_iface, session_bus)
        tracker_signal = TrackerSignal(dbus_path)
        loop = gobject.MainLoop()
        print "Running example signal emitter service."
    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)
    try:
            e = schedule.enter(0, 0, emit_tracker_signal, (sig1,  sig2,  delay,  ))
            schedule.run()
            loop.run()
    except (KeyboardInterrupt, dbus.DBusException, SystemExit):
            print "User requested exit... shutting down now"
            tracker_signal.Exit()
            pass
            sys.exit(0)
