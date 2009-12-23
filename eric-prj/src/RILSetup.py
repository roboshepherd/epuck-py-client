from math import pi

#RIL and AFM params
MAXSHOPTASK = 3
INIT_URGENCY = 0.5
DELTA_URGENCY = 0.01
DELTA_URGENCY_INC = 0.01
DELTA_URGENCY_DEC = 0.1
INIT_MATERIAL_COUNT = 10
XY = 2  # for task coordinates
DELTA_DISTANCE = 0.001
 
#robot device's instrinsics
INIT_SENSITIZATION = 0.1
INIT_LEARN_RATE = 0.01
INIT_FORGET_RATE = 0.0016
 
# for pose nomalization
MAX_X = 3600
MAX_Y = 3248
MAX_THETA = (2* pi)
 
# for navigation
TASK_RADIUS = 100 #pixel
TASK_CONE_ANGLE = 0.26 #15deg
MAX_NAV_STEP = 1 #how long navigation continues
