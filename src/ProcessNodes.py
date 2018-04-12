import os


"""
Instructions:

script_dir gives the dicrectory of this script (ProcessNodes.py). It is assumed that this scrpit is stored in a folder
which contains another folder for the input txt files (for me , the folder is script_dir/TSP/)  

"""
script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, 'TSP')

os.chdir(data_dir)

all_files = {}
for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
    for fname in filenames:
    	if fname[-3:] == "txt":
			print "Reading file: " + fname
    	current_txt = []
    	f = open(fname,"r")
    	f1 = f.readlines()
    	for line in f1:
    		line = line.split()
    		if line:
    			line = [int(i) for i in line]
    			current_txt.append(line)
    	all_files[fname] = current_txt


print all_files['att48.txt']

#TODO: finish this project
#Commit test from GKH
#William