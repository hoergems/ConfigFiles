import sys
import os
import subprocess
import glob
import argparse
import shutil

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-nO', '--numObstacles', type=int, default=5,
                    help='Number of obstacles')
parser.add_argument('-minc', '--minCovariance', type=float, default=0.0001, help="Minimum covariance")
parser.add_argument('-maxc', '--maxCovariance', type=float, default=0.01, help="Maximum covariance")
parser.add_argument('-cs', '--covarianceSteps', type=int, default=10, help="Number of covariance steps")
parser.add_argument('-nr', '--numRuns', type=int, default=100, help="Number of runs")
args = parser.parse_args()


numObstacles = args.numObstacles
robot = "4DOF"
robotExecName = "robot"
environmentTemplate = "4DOFFactory1.sdf"
 
minCovariance = float(args.minCovariance)
maxCovariance = float(args.maxCovariance)
covarianceSteps = int(args.covarianceSteps)
numRuns = int(args.numRuns)
    
covarianceStepSize = (maxCovariance - minCovariance) / (covarianceSteps - 1)
processCovariance = minCovariance
observationCovariance = minCovariance

folder = "cfg"
if os.path.isdir(folder):
    shutil.rmtree(folder)
os.makedirs(folder)

for i in xrange(1, covarianceSteps+1):
    for j in xrange(1, covarianceSteps+1):
	folder = "cfg" + "/" + str(i) + "_proc_" + str(j) + "_obs"
	os.makedirs(folder)
	for l in xrange(numRuns) :
	    with open("4DOFFactory1.cfg", 'r') as f:
		data = f.readlines()
		for k in xrange(len(data)):
		    if "minProcessCovariance" in data[k]:
			data[k] = "minProcessCovariance = " + str(processCovariance) + " \n"
		    elif "minObservationCovariance" in data[k]:
			data[k] = "minObservationCovariance = " + str(observationCovariance) + " \n"
		    elif "logPath" in data[k]:
			data[k] = "logPath = /datastore/hoe01h/WAFRJournal/4DOFFactory1/" + str(i) + "_proc_" + str(j) + "_obs/ \n"			
	            elif "logFilePostfix" in data[k]:
			data[k] = "logFilePostfix = " + str(l) + " \n"			
		with open(folder + "/4DOFFactory1_" + str(l) + ".cfg", 'a+') as l:
		    for k in xrange(len(data)):
			l.write(data[k])		
	observationCovariance += covarianceStepSize
    processCovariance += covarianceStepSize