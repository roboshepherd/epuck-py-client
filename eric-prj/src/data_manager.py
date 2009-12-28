import multiprocessing,  logging
class DataManager:
    def __init__(self):
        self.mgr = multiprocessing.Manager()
        self.mRobotPose = self.mgr.list() # to retrieve last  observed pose 
        self.mTaskInfo = self.mgr.dict() # key: taskid, value: list of attrib (t.s., x, y,  phi)
