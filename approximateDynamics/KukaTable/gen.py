import os


for i in xrange(2000):
    outFile = "KukaTable" + str(i) + ".cfg"    
    if os.path.isfile(outFile):
	os.remove(outFile)
    with open("KukaTable.cfg", 'r') as f:
	with open(outFile, 'a+') as of:	    
	    for line in f.readlines():
		if "logFilePostfix" in line:
		    of.write("logFilePostfix = " + str(i) + "\n")
		elif "outputFile =" in line:
		    of.write("outputFile = /data/hoe01h/oppt_devel/files/approximateDynamics/KukaTable/trajectorySamplesKukaTable" + str(i) + ".txt \n")
		elif "heuristicOutputFile = " in line:
		    of.write("heuristicOutputFile = /data/hoe01h/oppt_devel/files/approximateDynamics/KukaTable/heuristicSamplesKukaTable" + str(i) + ".txt \n")
		elif "numThreads =" in line:
		    of.write("numThreads = 6 \n")
		else:		    
		    of.write(line)   