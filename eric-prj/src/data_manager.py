import multiprocessing,  logging
class DataManager:
    def __init__(self):
        self.mgr = multiprocessing.Manager()
        self.mRobotPose = self.mgr.list() # to retrieve last  observed pose 
        self.mRobotPoseAvailable = self.mgr.Event() # set by dbus client
        self.mTaskInfo = self.mgr.dict() # key: taskid, value: list of attrib (t.s., x, y,  phi)
        self.mTaskInfoAvailable = self.mgr.Event() # set by dbus client
        self.mTaskSelected = self.mgr.Event() # Set/Unset by TaskSelector
        self.mTaskDoneOTO = self.mgr.Event()  # Set/Unset by DeviceController


