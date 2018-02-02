import glob
import os

outLines = []

for filename in glob.glob("heuristicSamples4DOFFactory1*"):
    if not "dynamic" in filename:
	with open(filename, 'r') as f:
	    for line in f.readlines():
		outLines.append(line)
outFile = "heuristicSamples4DOFFactory1Dynamic.txt"		
if os.path.isfile(outFile):
    os.remove(outFile)
with open(outFile, 'a+') as f:
    for line in outLines:
	outFile.write(line)