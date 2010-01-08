import subprocess
import re
import time
from data_manager import *

# Device status alias
DEVICE_NOT_RESPONDING = 0
DEVICE_AVAILABLE = 1
DEVICE_MOVING = 2
DEVICE_IDLE = 3
# globals
_packet_loss = ''
EXIT_COND = True 
# may be changed later to set as time duration 
SMALL_DELAY = 3

def process_ping_output(output):
    global _packet_loss
    pct = re.findall(r"\d\%", output)
    if(pct):
        print "%loss: ", pct[0]
    _packet_loss = pct[0]
    if (_packet_loss == '0%'):
        print "Device Alive"
        return True
    if (_packet_loss == '100%' or  (not _packet_loss)): 
        print "Device Dead"
        return False
    _packet_loss = ''

class DeviceController():
    def __init__(self,  dm,  bdaddr):
        self.datamgr_proxy = dm
        self.bdaddr = bdaddr
        self.l2ping_ok = False
        self.task_selected = False
        self.task_pending = False
        self.task_done = False
        self.task_timedout = False
        self.at_task = False
        self.pose_available = False
        # Device status
        self.status = DEVICE_NOT_RESPONDING

    def L2PingOK(self):
        # [CodeMakeup] Check if l2ping exits!
        cmd = "/usr/bin/l2ping -c " + " 1 " + bdaddr
        subproc = subprocess.Popen([cmd, ],\
            stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stdout_value = subproc.communicate()
        #print '\t got l2ping stdout_value:', stdout_value[0]
        self.l2ping_ok = process_ping_output(stdout_value[0])
        return self.l2ping_ok 

    def TaskSelected(self):
        val = False
        return val

    def TaskPending(self):
        val = False
        return val

    def TaskDone(self):
        val = False
        return val

    def TaskTimedOut(self):
        val = False
        return val

    def  AtTask(self):
        val = False
        return val

    def PoseAvailable(self):
        val = False
        return val

    def RunDeviceUnavailableLoop(self):
        while self.status is DEVICE_UNAVAILABLE:
            if self.L2PingOK():
                self.status = DEVICE_AVAILABLE # out loop
                self.RunDeviceAvailableLoop()
                break
            else: 
                self.status = DEVICE_UNAVAILABLE # stay here in loop
                time.sleep(SMALL_DELAY)

    def RunDeviceAvailableLoop(self):
        while self.status is DEVICE_AVAILABLE:
            if self.TaskSelected():
                self.status = DEVICE_MOVING
                self.RunDeviceMovingLoop() # go out of this loop
                break
            elif (not L2PingOK()):
                self.status = DEVICE_UNAVAILABLE
                self.RunDeviceUnavailableLoop() # go out of this loop
                break
            else:
               self.status = DEVICE_AVAILABLE # stay in-loop
               time.sleep(SMALL_DELAY)
   
    def RunDeviceMovingLoop(self):
        while self.status is DEVICE_MOVING:
            if TaskPending():
                self.task_pending = True
                if (not PoseAvailable()) or AtTask():
                    self.status = DEVICE_IDLE # go out of loop
                    self.RunDeviceIdleLoop()
                    break
                else :
                    self.status = DEVICE_MOVING # stay in-loop
                    # go to navigation routines for MoveToTarget or RandomWalk
            elif TaskDone() or TaskTimedOut():
                self.status = DEVICE_AVAILABLE # go out of loop
                self.RunDeviceAvailableLoop() 
            elif (not L2PingOK()):
                self.status = DEVICE_UNAVAILABLE # go out of loop
                self.RunDeviceUnavailableLoop()


    def RunDeviceIdleLoop(self):
        while self.status is DEVICE_IDLE:
            if not L2PingOK():
                self.status = DEVICE_UNAVAILABLE # go out of loop
                RunDeviceUnavailabeLoop()
                break
            elif TaskDone() or TaskTimedOut() or (not TaskPending()):  # FIX
                self.status = DEVICE_AVAILABLE # go out of loop
                RunDeviceAvailabeLoop()
                break
            elif  TaskPending() and PoseAvailable():
                self.status = DEVICE_MOVING # go out of loop
                RunDeviceMovingLoop()
                break
            elif TaskPending() and ( AtTask() or (not PoseAvailable())): 
                # stay in loop
                self.status = DEVICE_IDLE
                time.sleep(SMALL_DELAY)
            else:
                print "@RunDeviceIdleLoop: Unexpected situation "

    def RunMainLoop(self):
        while EXIT_COND:
            self.RunDeviceUnavailableLoop()


def get_config(config_file,  config):
    result = ' '
    f = open(config_file, 'r')
    data = f.read()
    lst = re.split(';', data)
    if (config == 'bdaddr'):
        result = lst[1]
    if(config == 'port'):
        result = lst[2]
    if(config == 'cfgfile'):
        result = lst[3]
    return result

def controller_main(data_mgr,  config_file):
        bdaddr = get_config(config_file,  'bdaddr')
        dc = DeviceController(data_mgr,  bdaddr)
        dc.RunMainLoop()
