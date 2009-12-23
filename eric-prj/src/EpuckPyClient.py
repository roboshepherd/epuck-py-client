#!/usr/bin/python
from pose import *
from epuck_navigator import *

def main():
    print "--- Start test---"
    n = EpuckNavigator()
    n.UpdateCurrentPose(200,  300,  2.5)
    n.GoToTaskLoc(2000,  2500)
    #n.UpdateNavFunc()
    print "--- End test---"

if __name__ == '__main__':
    main()

