import math,  time,  logging,  logging.config,  logging.handlers
from RILSetup import *
from data_manager import *
from ril_robot import *
from task_info import *

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("EpcLogger")

class Range():
    def __init__(self,  id):
        self.id = id
        self.start = 0
        self.end = 0

class TaskSelector():
    def __init__(self, dm,  robot): # taskinfo as recvd from dbus signal
        self.datamgr = dm
        self.robot =  robot
        self.taskinfo = dm.mTaskInfo
        self.stimulus = []
        self.probabilities = []
        self.taskranges = {} # put inst. of Range()es
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
        stimuli = math.tanh( 1 - (taskstimulus /  (taskcount + 1)))
        return stimuli

    def CalculateProbabilities(self):
        r = self.robot
        dm = self.datamgr
        #logger.debug("@TS Robot pose %s:" , dm.mRobotPose.items() )
        r.pose.UpdateFromList(dm.mRobotPose)
        logger.debug("@TS  Robot pose x=%f y=%f:" , r.pose.x,  r.pose.y )
        ti = self.taskinfo
        logger.debug("\t TaskInfo: %s",  ti.items() )
        taskCount = len(ti)
        logger.debug("\t task count %d:" , taskCount)
        try:
            for index,  info in ti.items():
                taskid = index 
                logger.info("Taskid -- %i:" ,  taskid)
                tx,  ty = info[TASK_INFO_X],  info[TASK_INFO_Y]
                dist = self.CalculateDist(r.pose,  tx, ty)
                logger.debug("\tTask dist %f:" ,  dist)
                learn =  r.taskrec[taskid].sensitization
                logger.debug("\tTask learn %f:" ,  learn)
                urg = info[TASK_INFO_URGENCY ]
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
        tsSum = math.fsum(self.stimulus)
        logger.debug("@TS Task Stimulus sum: %f",  tsSum)
        rwStimuli = self.CalculateRandomWalkStimuli(tsSum,  taskCount)
        logger.debug("@TS RandomWalk Stimuli: %f",  rwStimuli)
        taskid = 0
        r.taskrec[taskid].stimuli = rwStimuli
        stimulusSum = tsSum +  rwStimuli
        while taskid <= taskCount:
            pb =  r.taskrec[taskid].stimuli / stimulusSum
            r.taskrec[taskid].probability =pb
            logger.debug("@TS Task %d Prob %f",  taskid,  pb )
            taskid = taskid + 1
    
    def ConvertProbbToRange(self):
         robot = self.robot
         tasks = len(robot.taskrec)
         logger.debug("@TS Task Count including RW: %d",  tasks)
         startup = 0
         endsave = 0
         for taskid in range (tasks):
             end = robot.taskrec[taskid].probability * PROB_SCALE
             end = int(round(end)) + endsave
             r =  Range(taskid)
             r.start = startup
             r.end = end
             startup = end + 1
             endsave = end
             logger.debug("@TS Task %d prob start: %d  end: %d",  r.id, r.start, r.end )


    
    def SelectTask(self):
        self.CalculateProbabilities()
        self.ConvertProbbToRange()
        
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
    
