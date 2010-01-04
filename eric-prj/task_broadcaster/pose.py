#!/usr/bin/python
import math,  time,  logging,  logging.config,  logging.handlers
logging.config.fileConfig("logging.conf")
logger = logging.getLogger("EpcLogger")

class  Pose:
    info = {}
    def __init__(self,  ts=time.time(),  x=0,  y=0,  theta=0):
        self.ts = ts
        self.x = x 
        self.y = y 
        self.theta = theta
        self.info['ts'] = ts
        self.info['x'] = x
        self.info['y'] = y
        self.info['theta'] = theta
    
    def UpdateFromList(self,  pose):
        try:
            for k, v in pose.items():
                self.info[k] = v
                #logger.info("@Pose: Updating %s val: %f",  k,  v)  
            self.ts = self.info['ts']    
            self.x = self.info['x']
            self.y = self.info['y']
            self.theta = self.info['theta']
        except:
                logger.warn("Pose Update failed")
    
    
    def Update(self, poseinfo ):
        #"Pose Update TODO"
        try:
            self.info = poseinfo.copy()
            self.ts = poseinfo['ts']
            self.x =  poseinfo['x']
            self.y=  poseinfo['y']
            self.theta =  poseinfo['theta']
        except:
            print "Pose Update failed"
