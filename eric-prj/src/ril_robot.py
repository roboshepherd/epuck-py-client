from pose import *
from shop_task import *
from RILSetup import *
class TaskRecord:
    info = []
    def __init__(self,  id=-1,  sensitization=INIT_SENSITIZATION,  dist=0,  stimuli=0,  probability=0):
        self.id = id
        self.sensitization = sensitization
        self.dist = dist
        self.stimuli = stimuli
        self.probability = probability
    def Info(self):
        self.info = [self.id,  self.sensitization,   self.dist,  self.stimuli,  self.probability  ]
        return self.info

class RILRobot:
    taskrec = {}
    def __init__(self,  id=-1,  state=NOTSET,  pose=Pose(),\
                   lr=INIT_LEARN_RATE,  fr=INIT_FORGET_RATE, shoptask=ShopTask() ):             
        self.id = id
        self.state = state # device state
        self.pose = pose
        self.learnrate = lr
        self.forgetrate = fr
        self.shoptask = shoptask # currently doing task

    def InitTaskRecords(self,  taskcount):
        while taskcount >= 0:
            self.taskrec[taskcount] = TaskRecord(id=taskcount)
            taskcount = taskcount - 1
    
    def UpdatePose(self,  datamgr):
        if(datamgr.mRobotPose[0] is not 0): # default value changed
            self.pose.Update(datamgr.mRobotPose)
            #print self.pose.info
