import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))

from pyDbn import *

k = DBN(exportDir="../build/figures")
k.attach(NodeProperties(name="X",x=0, y=1,parents={1:"X"}))
k.attach(NodeProperties(name="Y",x=0, y=2,parents={0:"X"}, nodeType=NodeType.Observed, continuous=True))
k.attach(NodeProperties(name="\Sigma",x=0, y=3,parents={0:"Y"}, nodeType=NodeType.Variable))
k.attach(NodeProperties(name="\pi",x=0, y=0,parents={1:"X"}, nodeType=NodeType.Variable))
#k.export(sliceBefore=0, sliceAfter=3, centerSuffix="")
k.export(sliceBefore=2, sliceAfter=1, centerSuffix="\\tau")



