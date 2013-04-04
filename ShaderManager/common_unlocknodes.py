import pymel.core as pc

nodes = pc.ls(sl=1)

for node in nodes:
    pc.lockNode(node, lock=0)