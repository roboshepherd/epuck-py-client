#!/usr/bin/env python
import time, os, sys, sched, subprocess, re, signal, traceback
import gobject, dbus, dbus.service, dbus.mainloop.glib 
import multiprocessing,  logging,  logging.config
from RILSetup import DBUS_IFACE,  DBUS_PATH
from task_info import *
from pose import *
from data_manager import *
logging.config.fileConfig("logging.conf")
#create logger
logger = logging.getLogger("EpcLogger")

schedule = sched.scheduler(time.time, time.sleep)


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
        schedule.enter(inc, 0, emit_task_signal, (sig1,  inc)) # re-schedule to repeat this function
        global datamgr_proxy,  task_signal
        datamgr_proxy.mTaskInfoAvailable.wait()
        taskinfo = datamgr_proxy.mTaskInfo.copy() # use a soft copy
        datamgr_proxy.mTaskInfoAvailable.clear()
        #logging.debug("TaskInfo@Emitter: %s",  taskinfo)
        #print "\tEmitting TaskInfo signal>>> " 
        task_signal.TaskInfo(sig1,  taskinfo)
        taskinfo = None


def emitter_main(datamgr,  dbus_iface= DBUS_IFACE,  dbus_path = DBUS_PATH, \
        sig1= "TaskInfo",  delay = 3):
        global task_signal,  datamgr_proxy
        datamgr_proxy = datamgr
        # proceed only after taskinfo is populated
        datamgr_proxy.mTaskInfoAvailable.wait() 
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        session_bus = dbus.SessionBus()
        print "@Emitter-- TaskInfoAvailable %s" %datamgr_proxy.mTaskInfoAvailable.is_set() 
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
