import sys
import os
import subprocess
import glob
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-nO', '--numObstacles', type=int, default=5,
                    help='Number of obstacles')
parser.add_argument('-r', '--robot', type=str, default="Dubin", help="The robot")
args = parser.parse_args()


numObstacles = args.numObstacles
robot = args.robot
robotExecName = "dubin"
environmentTemplate = "maze_environment_random_"
maxCovariance = 0.01
if robot == "4DOF":
    robotExecName = "robot"
    environmentTemplate = "world_random_RobotImpl_"
    maxCovariance = 100.0
    
covarianceStepSize = (maxCovariance - 0.0001) / 9.0
covariance = 0.0001

if not os.path.isdir("cfg"):
	os.makedirs("cfg")	

for i in xrange(1, 11):
    with open(robot + ".cfg", 'r') as f:
	data = f.readlines()
	for j in xrange(len(data)):
	    if "minProcessCovariance" in data[j]:
		data[j] = "minProcessCovariance = " + str(covariance) + " \n"
	    elif "minObservationCovariance" in data[j]:
		data[j] = "minObservationCovariance = " + str(covariance) + " \n"
            elif "logPath" in data[j]:
		data[j] = "logPath = /datastore/hoe01h/WAFRJournal/randomScene/" + robot + "/collisionsNotAllowed/" + str(numObstacles) + "_obstacles/" + str(i) + " \n"
	if not os.path.isdir("cfg/" + str(i)):
	    os.makedirs("cfg/" + str(i))	    
	for j in xrange(100):
	    for k in xrange(len(data)):
		if "planningEnvironmentPath" in data[k]:		    
		    data[k] = "planningEnvironmentPath = " + environmentTemplate + str(numObstacles) + "_" + str(j) + ".sdf \n"
		if "executionEnvironmentPath" in data[k]:
		    data[k] = "executionEnvironmentPath = " + environmentTemplate + str(numObstacles) + "_" + str(j) + ".sdf \n"
            with open("cfg/" + str(i) + "/" + robot + str(j) + ".cfg", 'a+') as l:
		for k in xrange(len(data)):
		    l.write(data[k])	
	
        covariance += covarianceStepSize
