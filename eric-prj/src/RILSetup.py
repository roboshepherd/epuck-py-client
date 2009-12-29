from math import pi
# Enabling/Disabling Some Expt Settings/Params
USE_NORMALIZED_POSE = True

# DBus  RobotPose Message Protocol
TASK_INFO_TIME  = 0
TASK_INFO_X  = 1
TASK_INFO_Y  = 2
TASK_INFO_THETA = 3
TASK_INFO_PHI = 4


#D-Bus Config
DBUS_IFACE = "uk.ac.newport.ril.RobotTracker"
DBUS_PATH = "/robot1"

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
# angles
REVERSE_ANGLE1 = 2.90 
REVERSE_ANGLE2  = 1.52
DELTA_ANGLE1  = 0.26
DELTA_ANGLE0 =  0.26
 
ANGLE30  = pi/6
ANGLE90  = pi/2
ANGLE180 = pi
ANGLE270  = 3.0 * pi/2
ANGLE360  =  2.0 * pi

# Robot Device States
#/* Connectivity states */
NOTSET = -100
#/* state as (- id) e.g. UNAVAILABLE = - id
#UNAVAILABLE state of Robot 5 = - 5*/
UNAVAILABLE = -50
#/* state as (+ id) e.g. AVAILABLE = state + id
#AVAILABLE state of Robot 5 = 5*/
AVAILABLE = 0
#/* task states, set state as (this value+id) e.g. RW = 50 + id*/
RW = 50
TASK = 99 #/* seldom used */
TASK1 = 100
TASK2 = 200
TASK3 = 300
TASK4 = 400
TASK5 = 500
TASK6 = 600
TASK7 = 700
TASK8 = 800
TASK9 = 900
TASK10 = 1000
