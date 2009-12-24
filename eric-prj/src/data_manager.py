import multiprocessing,  logging
class DataManager:
    def __init__(self):
        self.mgr = multiprocessing.Manager()
        self.mRobotPose = self.mgr.dict() # to retrieve last  observed pose 
        # put as a dict where: key = timestamp, value: pose
        self.mTaskInfo = self.mgr.dict() # key: taskid, value: list of attrib (t.s., phi, posexy)
