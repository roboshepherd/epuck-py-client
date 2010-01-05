#!/usr/bin/env python
import time, os, sys, sched, subprocess, re, signal, traceback
import gobject, dbus, dbus.service, dbus.mainloop.glib 
import multiprocessing,  logging
from RILSetup import *
from data_manager import *
from utils import *

schedule = sched.scheduler(time.time, time.sleep)

#------------------ Signal Despatch ---------------------------------
class TaskStatusSignal(dbus.service.Object):
    def __init__(self, object_path):
        dbus.service.Object.__init__(self, dbus.SessionBus(), object_path)
    @dbus.service.signal(dbus_interface= DBUS_IFACE_EPUCK, signature='sis')
    def  TaskStatus(self,  sig,  taskid,  status):
        #logger.info("Emitted %s : Robot %d now %s ",  sig,  taskid,  status)
        #print "Emitted %s : Robot selected task %d now %s "  %(sig,  taskid,  status)
        pass
    def Exit(self):
        loop.quit()

    
def emit_task_selected_signal(delay,  sig1):
        global task_signal,  datamgr_proxy
        schedule.enter(delay, 0, emit_task_selected_signal, (delay, sig1  ) )
        #try:
        datamgr_proxy.mSelectedTaskAvailable.wait()
        taskdict = datamgr_proxy.mSelectedTask
        for k, v in taskdict.items():
            key = str(k)
            value = eval(str(v))
            print "From TaskDict got %s %i"  %(key,  value)
        sig = "TaskStatus"
        taskid =  value
        status = "Selected"
        task_signal.TaskStatus(sig,  taskid,  status)
#        except:
#            print "Emitting TaskStatus signal failed"
        #datamgr_proxy.mSelectedTaskAvailable.clear()


def server_main(dm,  dbus_iface= DBUS_IFACE_EPUCK,  dbus_path = DBUS_PATH_BASE, \
                sig1 = "TaskStatus",   delay = 3):
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    global task_signal,  datamgr_proxy
    datamgr_proxy = dm
    try:
        name = dbus.service.BusName(dbus_iface, session_bus)
        task_signal = TaskStatusSignal(dbus_path)
        loop = gobject.MainLoop()
        print "Running Outbound TaskStatus service."
    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)
    try:
            e = schedule.enter(0, 0, emit_task_selected_signal, (delay,  sig1,  ))
            schedule.run()
            loop.run()
    except (KeyboardInterrupt, dbus.DBusException, SystemExit):
            print "User requested exit... shutting down now"
            tracker_signal.Exit()
            pass
            sys.exit(0)
