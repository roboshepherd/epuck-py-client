import time
class Task:
    info = []
    def __init__(self, ts=time.time(),  x=300,  y=200,  theta=2.0,  phi=0.5 ):
        self.info.append (ts)
        self.info.append (x)
        self.info.append (y)
        self.info.append(theta)
        self.info.append (phi)
    def Print(self):
        print self.info

class TaskInfo:
    """Returns a dict with count no of taskinfo """
    def __init__(self,  count=1, ts=time.time(),  x=300,  y=200,  theta=2.0,  phi=0.5 ):
        d = {}
        seq = [i for i in range(count)]
        t = Task(ts=time.time(),  x=300,  y=200,  theta=2.0,  phi=0.5)
        val = [1 ,  2,  3]
        self.all = d.fromkeys(seq,  t.info)
        #print self.all
    
    def  Print(self):
        print self.all
        print " --- All task info printed ---"
    
