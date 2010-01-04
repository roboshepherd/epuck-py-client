import multiprocessing,  logging
from multiprocessing import *    
class DataManager:
    def __init__(self):
        self.tid = -1
        self.mgr = multiprocessing.Manager()
        self.mRobotPose = self.mgr.dict() # to retrieve last  observed pose 
        self.mRobotPoseAvailable = self.mgr.Event() # set by dbus client
        self.mTaskInfo = self.mgr.dict() # key: taskid, value: list of attrib (t.s., x, y,  phi)
        self.mTaskInfoAvailable = self.mgr.Event() # set by dbus client
        self.mSelectedTask = self.mgr.dict()  # Set/Unset by TaskSelector
        self.mSelectedTaskAvailable = self.mgr.Event() # Set/Unset by TaskSelector
        # DeviceController Signals
        self.mTaskDoneOTO = self.mgr.Event()  # Set/Unset by DeviceController
        #self.mDeviceNotResponding = 


