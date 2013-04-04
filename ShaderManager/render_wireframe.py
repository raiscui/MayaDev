import pymel.core as pc
from functools import partial

def prepareWireframe(selected):
    
    # List relatives
    relatives = pc.listRelatives(selected)
    
    # We scan if any relative is a group, if so we dig deeper
    for relative in relatives:
        if relative.type() == 'transform':
            prepareWireframe(relative)
            
        # We assign values if everything is ok
        elif relative.type() == 'mesh':
            
                
            # Get all the edges
            edgesList = [relative.edges[v] for v in range(len(relative.edges))]
            
            # Select edges and store them in a set
            pc.select(edgesList)
            wireSet = pc.sets(name='wireSet')
            
            # Smooth object
            subdiv = relative.smoothLevel.get()
            pc.polySmooth( edgesList, dv=subdiv)
#            
#            # Smooth normals
#            edgesList2 = [relative.edges[v] for v in range(len(relative.edges))]
#            pc.polySoftEdge(edgesList2, a=180)
#            
            # Select base edges and harden them
            pc.select(wireSet)
            pc.polySoftEdge(a=0)
#            
#            # Delete the set
#            pc.delete(wireSet)

    
# Get the selected objects
selections = pc.ls(sl=1)
    
# If none, execution stops here
if len(selections) == 0:
    pc.confirmDialog(t="Error", message="Nothing selected.", icon='critical')
# Else, we batch set the primary visibility 
else:
    print "### PROGRESS ### - Preparing Wireframe..."
    
    for sel in selections:
        prepareWireframe(sel)





