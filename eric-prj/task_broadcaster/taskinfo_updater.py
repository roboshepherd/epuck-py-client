from RILSetup import  *
from data_manager import *
from task_info import *
import multiprocessing,  logging,  logging.config
import time,  copy,  random

logging.config.fileConfig("logging.conf")
#create logger
logger = logging.getLogger("EpcLogger")

#  Setup Initial Task Info 
# TODO: Change it to reading from a config file
ti = TaskInfo()
task1 = ShopTask(id=1,  x=900,  y=1100)
task2 = ShopTask(id=2,  x=1500,  y=1200)
task3 = ShopTask(id=3,  x=2500,  y=1800)
ti.AddTaskInfo(1,  task1.Info()) 
ti.AddTaskInfo(2,  task2.Info())
ti.AddTaskInfo(3,  task3.Info())
taskinfo = copy.deepcopy(ti.all)

def GetTaskUrgency(taskid,  urg):
        global  datamgr_proxy
        workers = len(datamgr_proxy.mTaskWorkers[taskid])
        print "Task %d Workers:" %taskid
        print  datamgr_proxy.mTaskWorkers[taskid]
        if workers > 0:
            urgency = urg - workers * DELTA_TASK_URGENCY 
        else:
            urgency = urg +  DELTA_TASK_URGENCY 
        return urgency

def UpdateTaskInfo():
        global  datamgr_proxy
        print "DMP ti2 %s" %id(datamgr_proxy.mTaskInfo)
        #taskurg = taskurg - DELTA_TASK_URGENCY 
        for taskid, ti  in  datamgr_proxy.mTaskInfo.items():
            urg= ti[TASK_INFO_URGENCY] 
            ti[TASK_INFO_URGENCY] =   GetTaskUrgency(taskid,  urg)
            datamgr_proxy.mTaskInfo[taskid] = ti
            #print task
        datamgr_proxy.mTaskInfoAvailable.set() 
        print "Updated ti %s" %datamgr_proxy.mTaskInfo

def updater_main(datamgr):
        global datamgr_proxy,  taskurg
        datamgr_proxy = datamgr
        print "DMP ti1 %s" %id(datamgr_proxy.mTaskInfo)
        taskurg = INIT_TASK_URGENCY
        for k,  v in taskinfo.iteritems():
            datamgr_proxy.mTaskInfo[k] =v
            # simulating task worker signal recv.
            datamgr_proxy.mTaskWorkers[k] = [random.randint(1, 8)] * (k - 1)
        print "@updater:"
        print datamgr_proxy.mTaskInfo
        datamgr_proxy.mTaskInfoAvailable.set()
        while True:
            print "@updater:"
            UpdateTaskInfo()
            time.sleep(2)
