from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import random
from array import *
from odbAccess import openOdb
import odbAccess
import math
import numpy    
import os        # Operating system
import shutil    # copying or moving files

#Open text file to write results
sortie = open('RD.txt' , 'w')

odbname='Job-1'         # set odb name here
path='./'                    # set odb path here (if in working dir no need to change!)
myodbpath=path+odbname+'.odb'    
odb=openOdb(myodbpath)

for instanceName in odb.rootAssembly.instances.keys():
  print instanceName

topCenter = odb.rootAssembly.instances['PART-1-1']

fieldOutput = odb.steps['Step-1'].frames[-1].fieldOutputs['S']

field = fieldOutput.getSubset(region=topCenter, position=CENTROID)
    
fieldValues = field.values

for q in range (0,len(fieldValues)):
    S11 = fieldValues[q].data[0]
    S22 = fieldValues[q].data[1]
    S33 = fieldValues[q].data[2]
    S12 = fieldValues[q].data[3]
    S13 = fieldValues[q].data[4]
    S23 = fieldValues[q].data[5]
    elementLabel = odb.rootAssembly.instances['PART-1-1'].elements[q].label
    connectednodes = odb.rootAssembly.instances['PART-1-1'].elements[q].connectivity
    elementCentroidCoordinatesX = ((odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[0]-1)].coordinates[0] +
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[1]-1)].coordinates[0]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[2]-1)].coordinates[0]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[3]-1)].coordinates[0]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[4]-1)].coordinates[0]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[5]-1)].coordinates[0]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[6]-1)].coordinates[0]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[7]-1)].coordinates[0])/8)
    
    elementCentroidCoordinatesY = ((odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[0]-1)].coordinates[1] +
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[1]-1)].coordinates[1]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[2]-1)].coordinates[1]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[3]-1)].coordinates[1]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[4]-1)].coordinates[1]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[5]-1)].coordinates[1]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[6]-1)].coordinates[1]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[7]-1)].coordinates[1])/8)
    
    elementCentroidCoordinatesZ = ((odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[0]-1)].coordinates[2] +
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[1]-1)].coordinates[2]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[2]-1)].coordinates[2]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[3]-1)].coordinates[2]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[4]-1)].coordinates[2]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[5]-1)].coordinates[2]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[6]-1)].coordinates[2]+
    odb.rootAssembly.instances['PART-1-1'].nodes[(connectednodes[7]-1)].coordinates[2])/8)
    
    #sortie.write('%d ,%d,%d,%d,%d ,%d ,%d ,%d \n'%(connectednodes[0],connectednodes[1],connectednodes[2],connectednodes[3],connectednodes[4],connectednodes[5],connectednodes[6],connectednodes[7]))
    sortie.write('%d,%f,%f,%f,%f,%f,%f,%f,%f,%f\n' %(elementLabel,elementCentroidCoordinatesX,elementCentroidCoordinatesY,elementCentroidCoordinatesZ,S11,S22,S33,S12,S13,S23))


odb.close()
     
sortie.close()
