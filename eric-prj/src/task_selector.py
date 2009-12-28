import math
from RILSetup import *
class Range():
    def __init__(self):
        self.start = 0
        self.end = 0

class TaskSelector():
    def __init__(self, robot,  taskinfo): # taskinfo as recvd from dbus signal
        self.robot =  robot
        self.taskinfo = taskinfo
        self.stimulus = []
        self.probabilities = []
        self.taskranges = {} # put inst. of Range()
        self.selected_taskid = -1 
        self.deltadist = DELTA_DISTANCE

    def  CalculateDist(p1,  p2):
        x1 = p1.x
        y1 = p1.y
        x2 = p2.x
        y2 = p2.y
        return sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1));

    def CalculateStimuli(learn, dist, deltadist,  urgency):
        stimuli = tanh(learn * urgency / ( dist + deltadist))
        return stimuli

    def CalculateProbabilities(self):
        r = self.robot
        ti = self.taskinfo
        for taskid,  info in ti.iteritems():
            taskpose.x,  taskpose.y = info[1],  info[2]
            dist = CalculateDist(r.pose,  taskpose)
            learn = r.GetSensitization(taskid)
            urg =  r.taskrec(taskid).urgency
            stimuli = CalculateStimuli(learn, dist, self.deltadist, urg)
            self.stimulus.append(stimuli)
            # save claculation for logging and using in next step
            r.taskrec(taskid).id = taskid
            r.taskrec(taskid).sensitization = learn
            r.taskrec(taskid).dist = dist
            r.taskrec(taskid).stimuli = stimuli
        sum = fsum(self.stimulus)
        
