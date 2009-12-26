#!/usr/bin/python
import time
class  Pose:
    all = []
    def __init__(self,  ts=time.time(),  x=0,  y=0,  theta=0):
        self.ts = ts
        self.x = x 
        self.y = y 
        self.theta = theta
        self.all = [ts,  x,  y,  theta]
