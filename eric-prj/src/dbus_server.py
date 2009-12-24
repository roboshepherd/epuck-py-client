#!/usr/bin/env python
import time, os, sys, sched, subprocess, re, signal, traceback
import gobject, dbus, dbus.service, dbus.mainloop.glib 
import multiprocessing,  logging
from RILSetup import DBUS_IFACE,  DBUS_PATH

schedule = sched.scheduler(time.time, time.sleep)
posex = 300

class RobotSignal(dbus.service.Object):
    def __init__(self, object_path):
        dbus.service.Object.__init__(self, dbus.SessionBus(), object_path)
    @dbus.service.signal(dbus_interface= DBUS_IFACE, signature='sv')
    def RobotState(self, sig,  val):
        # The signal is emitted when this method exits
        # You can have code here if you wish
        #pass
        print "Now robot signal is: %s  val: %d " % (sig,  val)
    def Exit(self):
        loop.quit()

#Emit DBus-Signal
def emit_dbus_signal(sig,  inc):
    schedule.enter(inc, 0, emit_dbus_signal, (sig,  inc)) # re-schedule to repeat this function
    global dbus_signal,  posex
    print "Emitting signal>>> " 
    dbus_signal.RobotState(sig,  posex)

def server_main(dbus_iface= DBUS_IFACE,  dbus_path = DBUS_PATH,  sig = "RobotState", delay = 1):
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    global dbus_signal
    try:
        name = dbus.service.BusName(dbus_iface, session_bus)
        dbus_signal = RobotSignal(dbus_path)
        loop = gobject.MainLoop()
        print "Running example signal emitter service."
    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)
    try:
            e = schedule.enter(0, 0, emit_dbus_signal, (sig,  delay))
            schedule.run()
            loop.run()
    except (KeyboardInterrupt, dbus.DBusException, SystemExit):
            print "User requested exit... shutting down now"
            dbus_signal.Exit()
            pass
            sys.exit(0)
