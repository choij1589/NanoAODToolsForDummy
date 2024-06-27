#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

print('Hello We are going to merging')



from PhysicsTools.NanoAODTools.postprocessing.utils.crabhelper import inputFiles, runsAndLumis
print(inputFiles())
p=PostProcessor(
  ".",
  inputFiles(), provenance=True,
  prefetch = True
)
p.run()
print('Done')
os.system("ls -lR")