import os
dataset22 = []
dataset22EE = []
with open('MC.txt') as f:
	lines = f.readlines()
	for line in lines:
		dataset = line.replace('\n','')
		if 'EE' in dataset:
			dataset22EE.append(dataset)
		else:
			dataset22.append(dataset)
dataset22 = set(dataset22)
dataset22EE = set(dataset22EE)

#write to file

with open('MC_2022.txt','w') as f:
	for dataset in dataset22:
		f.write(dataset+'\n')
with open('MC_2022EE.txt','w') as f:
	for dataset in dataset22EE:
		f.write(dataset+'\n')