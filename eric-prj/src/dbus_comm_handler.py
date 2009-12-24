import time, os, sys, sched, subprocess, re, signal, traceback
import gobject, dbus, dbus.service, dbus.mainloop.glib 
import multiprocessing,  logging
from RILSetup import DBUS_IFACE,  DBUS_PATH

def robot_signal_handler( sig,  val):
    print "Caught signal  %s (in robot signal handler) %d "  %(sig,  val)
 

def main_loop():
    try:
        loop = gobject.MainLoop()
        loop.run()
    except (KeyboardInterrupt, SystemExit):
        print "User requested exit... shutting down now"
        pass
        sys.exit(0)

def client_main(data_mgr,  dbus_iface= DBUS_IFACE,  dbus_path = DBUS_PATH,  sig = "RobotState"):
     dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
     bus = dbus.SessionBus()
     try:
        #bus_object = bus.get_object(dbus_iface, dbus_path)
        #bus_object.connect_to_signal(sig, robot_signal_handler, dbus_interface=dbus_iface)
        bus.add_signal_receiver(robot_signal_handler, dbus_interface = DBUS_IFACE, signal_name = sig)
        main_loop()
     except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)
