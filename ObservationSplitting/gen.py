import sys
import os
import subprocess
import glob
import argparse
import shutil
from random import randint
import shutil

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-nO', '--numObstacles', type=int, default=5,
                    help='Number of obstacles')
parser.add_argument('-minc', '--minCovariance', type=float, default=0.0001, help="Minimum covariance")
parser.add_argument('-maxc', '--maxCovariance', type=float, default=0.01, help="Maximum covariance")
parser.add_argument('-cs', '--covarianceSteps', type=int, default=10, help="Number of covariance steps")
parser.add_argument('-nr', '--numRuns', type=int, default=100, help="Number of runs")
parser.add_argument('-ct', '--environmentTemplate', type=str, default="4DOFFactory1", help="The config file to process")
parser.add_argument('-rp', '--resultsPath', type=str, default="/datastore/hoe01h/WAFRJournal", help="The path where the log files are stored in")
args = parser.parse_args()


numObstacles = args.numObstacles
robot = "4DOF"
robotExecName = "robot"
environmentTemplate = args.environmentTemplate
resultsPath = args.resultsPath
if (resultsPath.strip()[-1] != "/"):
    resultsPath += "/"
 
minCovariance = float(args.minCovariance)
maxCovariance = float(args.maxCovariance)
covarianceSteps = int(args.covarianceSteps)
numRuns = int(args.numRuns)
    
covarianceStepSize = 0.0
if (covarianceSteps > 1):    
    covarianceStepSize = (maxCovariance - minCovariance) / (covarianceSteps - 1)
processCovariance = minCovariance
observationCovariance = minCovariance

folder = "cfg"
if not os.path.isdir(folder):    
    os.makedirs(folder)

for i in xrange(1, covarianceSteps+1):
    observationCovariance = minCovariance    
    folder = "cfg/" + str(i) + "_dist"
    if os.path.isdir(folder):
	shutil.rmtree(folder)
    os.makedirs(folder)
    for l in xrange(numRuns) :
	with open(environmentTemplate + ".cfg", 'r') as f:
	    data = f.readlines()                
	    for k in xrange(len(data)):		
		elif "logPath" in data[k]:
		    dr = resultsPath + environmentTemplate + "/" + str(i) + "_dist/"
		    data[k] = "logPath = " + dr + " \n"
		    if not os.path.exists(dr):
			os.makedirs(dr)
		elif "logFilePostfix" in data[k]:
		    data[k] = "logFilePostfix = " + str(l) + " \n"		
	    with open(folder + "/" + environmentTemplate + "_" + str(l) + ".cfg", 'a+') as l:		
		for k in xrange(len(data)):
		    l.write(data[k])		
	observationCovariance += covarianceStepSize
	processCovariance += covarianceStepSize
