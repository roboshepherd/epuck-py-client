#!/usr/bin/env python
import time, os, sys, sched, subprocess, re, signal, traceback
import gobject, dbus, dbus.service, dbus.mainloop.glib 
import multiprocessing,  logging
from RILSetup import DBUS_IFACE,  DBUS_PATH
from task_info import *


schedule = sched.scheduler(time.time, time.sleep)
posets = time.time()
posex = 300
posey = 200
posetheta = 2.0
taskinfo = TaskInfo(2).all

class TrackerSignal(dbus.service.Object):
    def __init__(self, object_path):
        dbus.service.Object.__init__(self, dbus.SessionBus(), object_path)
        #global taskinfo
    @dbus.service.signal(dbus_interface= DBUS_IFACE, signature='sdddd')
    def RobotPose(self, sig,  ts,  x,  y,  theta):
        # The signal is emitted when this method exits
        #pass
        print "Tracker signal: %s" %sig
        print" %0.2f, %.2f, %.2f, %.2f " %  (ts,  x,  y,  theta)
    @dbus.service.signal(dbus_interface= DBUS_IFACE, signature='sa{iad}')
    def TaskInfo(self, sig,  taskinfo):
        # The signal is emitted when this method exits
        print "Tracker signal: %s  " % (sig)
        print taskinfo
    def Exit(self):
        loop.quit()

#Emit DBus-Signal
def emit_tracker_signal(sig,  inc,  taskinfo):
    print "At emit_tracker_signal():"
    #taskinfo.Print()
    global tracker_signal,  posets,  posex,  posey,  posetheta
    schedule.enter(inc, 0, emit_tracker_signal, (sig,  inc,  taskinfo, )) # re-schedule to repeat this function
    print "\tEmitting signal>>> " 
    #taskinfo.Print()
    tracker_signal.TaskInfo("TaskInfo",  taskinfo)
    tracker_signal.RobotPose(sig,  posets,  posex,  posey,  posetheta)

def server_main(dbus_iface= DBUS_IFACE,  dbus_path = DBUS_PATH,  sig = "RobotState", delay = 1):
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
            e = schedule.enter(0, 0, emit_tracker_signal, (sig,  delay,  taskinfo, ))
            schedule.run()
            loop.run()
    except (KeyboardInterrupt, dbus.DBusException, SystemExit):
            print "User requested exit... shutting down now"
            tracker_signal.Exit()
            pass
            sys.exit(0)
