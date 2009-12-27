import time

class Task:
    info = []
    def __init__(self, id,  x,  y,    theta=0.0,  phi=0.5,  ts=time.time() ):
        self.id = id 
        self.x = x
        self.y = y
        self.theta = theta
        self.phi = phi
        self.ts = ts
    def Info(self):
        self.info = [self.ts,  self.x,  self.y,  self.theta,  self.phi]
        return self.info
