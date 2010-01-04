from data_manager import *
from task_info import *

ti = TaskInfo()
task1 = ShopTask(id=1,  x=900,  y=1100)
task2 = ShopTask(id=2,  x=1500,  y=1200)
task3 = ShopTask(id=3,  x=2500,  y=1800)
ti.AddTaskInfo(1,  task1.Info()) 
ti.AddTaskInfo(2,  task2.Info())
ti.AddTaskInfo(3,  task3.Info())
taskinfo = ti.all

#def UpdateTaskInfo():
        

def updater_main(datamgr):
        global datamgr_proxy
        datamgr_proxy = datamgr
        datamgr_proxy.mTaskInfo = taskinfo
        datamgr_proxy.mTaskInfoAvailable.set()
        #print taskinfo
        
        while True:
            print "@updater:"
            print datamgr_proxy.mTaskInfo
            time.sleep(2)
   
