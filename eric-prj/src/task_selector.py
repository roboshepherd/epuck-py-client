import math,  time,  logging,  logging.config,  logging.handlers
from RILSetup import *
from data_manager import *
from ril_robot import *
from task_info import *

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("EpcLogger")

class Range():
    def __init__(self):
        self.start = 0
        self.end = 0

class TaskSelector():
    def __init__(self, dm,  robot): # taskinfo as recvd from dbus signal
        self.datamgr = dm
        self.robot =  robot
        self.taskinfo = dm.mTaskInfo
        self.stimulus = []
        self.probabilities = []
        self.taskranges = {} # put inst. of Range()
        self.selected_taskid = -1 
        self.deltadist = DELTA_DISTANCE

    def  CalculateDist(self,  rp,  tx,  ty):
        if USE_NORMALIZED_POSE == True:
            x1 = rp.x/(MAX_X * 10)
            y1 = rp.y/(MAX_Y * 10)
            x2 = tx/(MAX_X * 10)
            y2 = ty/(MAX_Y * 10)
        else:
            x1 = rp.x
            y1 = rp.y
            x2 = tx
            y2 = ty
        return math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))

    def CalculateTaskStimuli(self,  learn, dist, deltadist,  urgency):
        stimuli = math.tanh(learn * urgency / ( dist + deltadist))
        return stimuli
    
    def CalculateRandomWalkStimuli(self,  taskstimulus,  taskcount):
        stimuli = math.tanh( 1 - taskstimulus /  (taskcount + 1))
        return stimuli

    def CalculateProbabilities(self):
        r = self.robot
        dm = self.datamgr
        #logger.debug("@TS Robot pose %s:" , dm.mRobotPose.items() )
        r.pose.UpdateFromList(dm.mRobotPose)
        logger.debug("@TS  Robot pose x=%f y=%f:" , r.pose.x,  r.pose.y )
        ti = self.taskinfo
        logger.debug("\t TaskInfo: %s",  ti.items() )
        taskcount = len(ti)
        logger.debug("\t taskcount %d:" , taskcount)
        try:
            for index,  info in ti.items():
                taskid = index 
                logger.info("Taskid -- %i:" ,  taskid)
                tx,  ty = info[1],  info[2]
                dist = self.CalculateDist(r.pose,  tx, ty)
                logger.debug("\tTask dist %f:" ,  dist)
                learn =  r.taskrec[taskid].sensitization
                logger.debug("\tTask learn %f:" ,  learn)
                urg = info[4]
                logger.debug("\tTask urg %f:" ,  urg)
                stimuli = self.CalculateTaskStimuli(learn, dist, self.deltadist, urg)
                logger.debug("\tTask stimuli %f:" ,  stimuli)
                self.stimulus.append(stimuli)
                # save claculation for logging and using in next step
                r.taskrec[taskid].id = taskid
                r.taskrec[taskid].sensitization = learn
                r.taskrec[taskid].dist = dist
                r.taskrec[taskid].stimuli = stimuli
        except:
            logger.error("FIXME --  list error")
        sum = math.fsum(self.stimulus)
        logger.debug("Stimulus sum: %f",  sum)
        rwStimuli = self.CalculateRandomWalkStimuli(sum,  taskcount)
        logger.debug("RandomWalk Stimuli: %f",  rwStimuli)
    
    def SelectTask(self):
        self.CalculateProbabilities()
        
# main process function
def  selector_main(dataManager,  robot):
    #time.sleep(INIT_SLEEP)
    ts = TaskSelector(dataManager,  robot)
    while True:
        dataManager.mRobotPoseAvailable.wait()
        #logger.debug("Robot psoe.x:%d ",  ts.robot.pose.x )
        dataManager.mTaskInfoAvailable.wait()
        #logger.debug("@TS TaskInfo Dictlen %d",  len(dataManager.mTaskInfo))
        #l =  len(dataManager.mRobotPose )
        #logger.debug("@TS Robot pose dict len %d:" , l)
        #logger.debug("@TS Robot pose %s:" , dataManager.mRobotPose.items() )
        ts.SelectTask() # can be started delayed
        dataManager.mTaskDoneOTO.wait() # task done or timedout
    