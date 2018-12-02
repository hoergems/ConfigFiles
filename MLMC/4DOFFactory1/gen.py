import sys
import os
import subprocess
import glob
import argparse
import shutil
from random import randint
import shutil

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-nr', '--numRuns', type=int, default=100, help="Number of runs")
parser.add_argument('-ct', '--environmentTemplate', type=str, default="4DOFFactory1", help="The config file to process")
parser.add_argument('-rp', '--resultsPath', type=str, default="/datastore/hoe01h/WAFRJournal", help="The path where the log files are stored in")
args = parser.parse_args()

environmentTemplate = args.environmentTemplate
resultsPath = args.resultsPath
if (resultsPath.strip()[-1] != "/"):
    resultsPath += "/"
numRuns = int(args.numRuns)

folder = "cfg"
if not os.path.isdir(folder):    
    os.makedirs(folder)
folder = "cfg/"
if os.path.isdir(folder):
    shutil.rmtree(folder)
os.makedirs(folder)

times = [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
algs = ["noCorrection", "bias", "correction", "pomcp"]
for time in times:
    for alg in algs:
        for l in xrange(numRuns):
            with open(environmentTemplate + ".cfg", 'r') as f:
                data = f.readlines()
                for k in xrange(len(data)):
                    if "logPath" in data[k]:
                        dr = resultsPath + environmentTemplate + "/"
                        data[k] = "logPath = " + dr + " \n"
                        if not os.path.exists(dr):
                            os.makedirs(dr)
                    elif "logFilePostfix" in data[k]:
                        data[k] = "logFilePostfix = " + alg + "_" + str(time) + "_" + str(l) + " \n"
                    elif "planningSimulationStepSize" in data[k]:
                        if alg == "noCorrection":
                            data[k] = "planningSimulationStepSize = 0.0 \n"
                        elif alg == "bias":
                            data[k] = "planningSimulationStepSize = 0.02 \n"
                        elif alg == "correction":
                            data[k] = "planningSimulationStepSize = 0.02 \n"
                        elif alg == "pomcp":
                            data[k] = "planningSimulationStepSize = 0.0 \n"
                    elif "mlmc" in data[k]:
                        if alg == "noCorrection":
                            data[k] = "mlmc = false \n"
                        elif alg == "bias":
                            data[k] = "mlmc = false \n"
                        elif alg == "correction":
                            data[k] = "mlmc = true \n"
                    elif "stepTimeout" in data[k]:
                        data[k] = "stepTimeout = " + str(time) + "\n"
                cfgFile = folder + "/" + environmentTemplate + "_" + alg + "_" + str(time) + "_" + str(l) + ".cfg"
                print cfgFile
                with open(cfgFile, 'a+') as l:
                    print "open " + cfgFile
                    for k in xrange(len(data)):
                        l.write(data[k])