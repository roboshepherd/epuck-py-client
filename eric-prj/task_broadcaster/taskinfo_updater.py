from data_manager import *
from task_info import *
import multiprocessing,  logging,  logging.config
import time 
import copy 

logging.config.fileConfig("logging.conf")
#create logger
logger = logging.getLogger("EpcLogger")

#  Setup Initial Task Info
ti = TaskInfo()
task1 = ShopTask(id=1,  x=900,  y=1100)
task2 = ShopTask(id=2,  x=1500,  y=1200)
task3 = ShopTask(id=3,  x=2500,  y=1800)
ti.AddTaskInfo(1,  task1.Info()) 
ti.AddTaskInfo(2,  task2.Info())
ti.AddTaskInfo(3,  task3.Info())
taskinfo = copy.deepcopy(ti.all)

#def UpdateTaskInfo():
        

def updater_main(datamgr):
        global datamgr_proxy
        datamgr_proxy = datamgr
        for k,  v in taskinfo.iteritems():
            datamgr_proxy.mTaskInfo[k] =v
        print "@updater:"
        print datamgr_proxy.mTaskInfo
        datamgr_proxy.mTaskInfoAvailable.set()
        for i in range(3):
            logger.debug("DMPu %s",  datamgr_proxy)
            logger.debug("DMPu ti  %s",  type(datamgr_proxy.mTaskInfo) )
            time.sleep(5)
   
