import time

class ShopTask:
    info = []
    pose = []
    workers = []
    def __init__(self, id=-1,  x=0,  y=0,    theta=0.0,  phi=0.5,  ts=time.time() ):
        self.id = id 
        self.x = x
        self.y = y
        self.theta = theta
        self.phi = phi
        self.ts = ts
    def Info(self):
        self.info = [self.ts,  self.x,  self.y,  self.theta,  self.phi]
        return self.info
    def  Pose(self):
        self.pose = [self.x,  self.y,  self.theta]
        return self.pose
    def Workers(self):
        return self.workers 
