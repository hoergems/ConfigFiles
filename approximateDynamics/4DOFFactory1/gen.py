import os


for i in xrange(1000):
    outFile = "4DOFFactory1ApproxMax" + str(i) + ".cfg"
    if os.path.isfile(outFile):
	os.remove(outFile)
    with open("4DOFFactory1ApproxMax.cfg", 'r') as f:
	with open(outFile, 'a+') as of:	    
	    for line in f.readlines():
		if "logFilePostfix" in line:
		    of.write("logFilePostfix = " + str(i) + "\n")
		elif "outputFile =" in line:
		    of.write("outputFile = /data/hoe01h/oppt_devel/files/approximateDynamics/trajectorySamples4DOFFactory1" + str(i) + ".txt \n")
		elif "heuristicOutputFile = " in line:
		    of.write("heuristicOutputFile = /data/hoe01h/oppt_devel/files/approximateDynamics/heuristicSamples4DOFFactory1" + str(i) + ".txt \n")
		elif "numThreads =" in line:
		    of.write("numThreads = 6 \n")
		else:		    
		    of.write(line)   