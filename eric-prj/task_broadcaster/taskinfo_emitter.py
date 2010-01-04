#!/usr/bin/env python
import time, os, sys, sched, subprocess, re, signal, traceback
import gobject, dbus, dbus.service, dbus.mainloop.glib 
import multiprocessing,  logging
from RILSetup import DBUS_IFACE,  DBUS_PATH
from task_info import *
from pose import *

schedule = sched.scheduler(time.time, time.sleep)
# initialize taskinfo
ti = TaskInfo()
task1 = ShopTask(id=1,  x=900,  y=1100)
task2 = ShopTask(id=2,  x=1500,  y=1200)
task3 = ShopTask(id=3,  x=2500,  y=1800)
ti.AddTaskInfo(1,  task1.Info()) 
ti.AddTaskInfo(2,  task2.Info())
ti.AddTaskInfo(3,  task3.Info())
taskinfo = ti.all

class TaskInfoSignal(dbus.service.Object):
    def __init__(self, object_path):
        dbus.service.Object.__init__(self, dbus.SessionBus(), object_path)
    @dbus.service.signal(dbus_interface= DBUS_IFACE, signature='sa{iad}')
    def TaskInfo(self, sig,  taskinfo):
        # The signal is emitted when this method exits
        print "TaskInfo signal: %s  " % (sig)
        print taskinfo
    def Exit(self):
        loop.quit()

#Emit DBus-Signal
def emit_task_signal(sig1,  inc):
    print "At emit_task_signal():"
    global task_signal,   taskinfo
    schedule.enter(inc, 0, emit_task_signal, (sig1,  inc)) # re-schedule to repeat this function
    print "\tEmitting TaskInfo signal>>> " 
    task_signal.TaskInfo(sig1,  taskinfo)


def emitter_main(dbus_iface= DBUS_IFACE,  dbus_path = DBUS_PATH, \
               sig1= "TaskInfo",  delay = 3):
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    global task_signal,  taskinfo
    try:
        name = dbus.service.BusName(dbus_iface, session_bus)
        task_signal = TaskInfoSignal(dbus_path)
        loop = gobject.MainLoop()
        print "Running taskinfo signal emitter service."
    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)
    try:
            e = schedule.enter(0, 0, emit_task_signal, (sig1,  delay,  ))
            schedule.run()
            loop.run()
    except (KeyboardInterrupt, dbus.DBusException, SystemExit):
            print "User requested exit... shutting down now"
            task_signal.Exit()
            pass
            sys.exit(0)
