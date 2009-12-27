import time

from task import *

class TaskInfo:
    """Returns a dict with  taskinfo """
    all = {}
    def __init__(self):
        pass

    
    def AddTaskInfo(self,  id,  taskinfo):
        self.all[id] = taskinfo

    def  Print(self):
        print self.all
        print " --- All task info printed ---"
    
