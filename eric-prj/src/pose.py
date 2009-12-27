#!/usr/bin/python
import time
class  Pose:
    info = []
    def __init__(self,  ts=time.time(),  x=0,  y=0,  theta=0):
        self.ts = ts
        self.x = x 
        self.y = y 
        self.theta = theta
        self.info = [ts,  x,  y,  theta]
    
    def Update(self, poseinfo ):
        self.info = poseinfo
        self.ts = poseinfo[0]
        self.x =  poseinfo[1]
        self.y=  poseinfo[2]
        self.theta =  poseinfo[3]
