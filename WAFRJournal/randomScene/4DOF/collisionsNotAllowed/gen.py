import sys
import os
import subprocess
import glob
import argparse
import shutil

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-nO', '--numObstacles', type=int, default=5,
                    help='Number of obstacles')
parser.add_argument('-r', '--robot', type=str, default="Dubin", help="The robot")
parser.add_argument('-minc', '--minCovariance', type=float, default=0.0001, help="Minimum covariance")
parser.add_argument('-maxc', '--maxCovariance', type=float, default=0.01, help="Maximum covariance")
parser.add_argument('-cs', '--covarianceSteps', type=int, default=10, help="Number of covariance steps")
parser.add_argument('-nr', '--numRuns', type=int, default=100, help="Number of runs")
args = parser.parse_args()


numObstacles = args.numObstacles
robot = args.robot
robotExecName = "dubin"
environmentTemplate = "maze_environment_random_"
if robot == "4DOF":
    robotExecName = "robot"
    environmentTemplate = "world_random_RobotImpl_"
 
minCovariance = float(args.minCovariance)
maxCovariance = float(args.maxCovariance)
covarianceSteps = int(args.covarianceSteps)
numRuns = int(args.numRuns)
    
covarianceStepSize = (maxCovariance - minCovariance) / (covarianceSteps - 1)
covariance = minCovariance

folder = str(numObstacles) + "_obstacles"

if os.path.isdir(folder):
    shutil.rmtree(folder)
os.makedirs(folder)
os.makedirs(folder + "/cfg")
	

for i in xrange(1, covarianceSteps + 1):
    with open(robot + ".cfg", 'r') as f:
	data = f.readlines()
	for j in xrange(len(data)):
	    if "minProcessCovariance" in data[j]:
		data[j] = "minProcessCovariance = " + str(covariance) + " \n"
	    elif "minObservationCovariance" in data[j]:
		data[j] = "minObservationCovariance = " + str(covariance) + " \n"
            elif "logPath" in data[j]:
		data[j] = "logPath = /datastore/hoe01h/WAFRJournal/randomScene/" + robot + "/collisionsNotAllowed/" + str(numObstacles) + "_obstacles/" + str(i) + " \n"
	if not os.path.isdir(folder + "/cfg/" + str(i)):
	    os.makedirs(folder + "/cfg/" + str(i))	    
	for j in xrange(numRuns):
	    for k in xrange(len(data)):
		if "planningEnvironmentPath" in data[k]:		    
		    data[k] = "planningEnvironmentPath = " + environmentTemplate + str(numObstacles) + "_" + str(j) + ".sdf \n"
		if "executionEnvironmentPath" in data[k]:
		    data[k] = "executionEnvironmentPath = " + environmentTemplate + str(numObstacles) + "_" + str(j) + ".sdf \n"	    
            '''if os.path.isfile(folder + "/cfg/" + str(i) + "/" + robot + str(j) + ".cfg"):
		os.remove(folder + "/cfg/" + str(i) + "/" + robot + str(j) + ".cfg")'''
            with open(folder + "/cfg/" + str(i) + "/" + robot + str(j) + ".cfg", 'a+') as l:
		for k in xrange(len(data)):
		    l.write(data[k])	
	
        covariance += covarianceStepSize
