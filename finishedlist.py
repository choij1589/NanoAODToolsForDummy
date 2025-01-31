import os

def makeCopysh(listdir, targetlist,filename):
    copys=[]
    for dir in listdir:
    #if some element in targetlist contain the string of dir.split("/")[-1], then copy the dir to the target directory
        if any([dir.split("/")[-1] == x for x in targetlist]):
            #get matched element x
            x = [x for x in targetlist if dir.split("/")[-1] in x][0]
            #check era
            if '23' in x:
                era = '2023'
            elif '22' in x:
                era = '2022'
                
            
            if '2022EE' in x:
                era = '2022EE'
            if 'BPix' in x:
                era = '2023BPix'
            #check MC or data
            isMC = True
            if 'EGamma' in dir or 'Muon' in dir or 'JetMET' in dir:
                isMC = False
            if not isMC:
                period = "Period"+x.split("_")[2][-1]
                sampleName = dir.split("_")[-1]
                targetDir = f"/gv0/Users/yeonjoon/DATA/SKFlat/Run3NanoAODv12/{era}/DATA/{sampleName}/{period}"
            else:
                sampleName = x.replace(f"crab_{era}_", "")
                targetDir = f"/gv0/Users/yeonjoon/DATA/SKFlat/Run3NanoAODv12/{era}/MC/{sampleName}"
                
            
            if not os.path.isdir(targetDir):
                os.makedirs(targetDir)
                print(f"will make {targetDir}")
            
            #search the listdir and find the directory under the dir. depth == 1.
            copydir = []
            for subdir in listdir:
                if subdir.startswith(dir) and subdir.count("/") == dir.count("/") + 1:
                    copydir.append(subdir)
            for subdir in copydir:
                copys.append(f"xrdcp -r --parallel 4 ---retry 5 root://cluster142.knu.ac.kr/{subdir} {targetDir}")
           

    with open(filename, "w") as f:
        for copy in copys:
            f.write(copy)
            f.write("\n")
        
loglist = os.listdir("./")
loglist = [x for x in loglist if x.endswith(".log")]
loglist = [x for x in loglist if not "With" in x]
endlist = []
notendlist = []
for log in loglist:
    with open(log, "r") as f:
        lines = f.readlines()
        #if file contains "100.0%", add it to endlist
        #if not, add it to notendlist
        if any(["100.0%" in x for x in lines]):
            endlist.append(log.replace(".log", ""))
        else:
            notendlist.append(log.replace(".log", ""))
listdir = os.popen(f"xrdfs cluster142.knu.ac.kr ls -R /store/user/yeonjoon/SKNano_0105").readlines()
listdir = [x.replace("\n", "") for x in listdir if not x.endswith(".root")]
makeCopysh(listdir, endlist, "copy.sh")
makeCopysh(listdir, notendlist, "notendcopy.sh")


            
            
        
        