import sys
import os
import subprocess
import glob

covarianceStepSize = (0.01 - 0.0001) / 9.0
covariance = 0.0001
numObstacles = 10

if not os.path.isdir("cfg"):
	os.makedirs("cfg")	

for i in xrange(1, 11):
    with open("dubin.cfg", 'r') as f:
	data = f.readlines()
	for j in xrange(len(data)):
	    if "minProcessCovariance" in data[j]:
		data[j] = "minProcessCovariance = " + str(covariance) + " \n"
	    elif "minObservationCovariance" in data[j]:
		data[j] = "minObservationCovariance = " + str(covariance) + " \n"
            elif "logPath" in data[j]:
		data[j] = "logPath = /datastore/hoe01h/WAFRJournal/randomScene/Dubin/collisionsNotAllowed/" + str(numObstacles) + "_obstacles/" + str(i) + " \n"
	if not os.path.isdir("cfg/" + str(i)):
	    os.makedirs("cfg/" + str(i))	    
	for j in xrange(100):
	    for k in xrange(len(data)):
		if "planningEnvironmentPath" in data[k]:		    
		    data[k] = "planningEnvironmentPath = maze_environment_random_" + str(numObstacles) + "_" + str(j) + ".sdf \n"
		if "executionEnvironmentPath" in data[k]:
		    data[k] = "executionEnvironmentPath = maze_environment_random_" + str(numObstacles) + "_" + str(j) + ".sdf \n"
            with open("cfg/" + str(i) + "/dubin" + str(j) + ".cfg", 'a+') as l:
		for k in xrange(len(data)):
		    l.write(data[k])	
	
        covariance += covarianceStepSize
