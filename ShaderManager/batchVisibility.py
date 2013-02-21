import pymel.core as pc

# Dictionnary that contains all UI elements
uiWidgets = {}

primaryVisibility = True

# Explore recursively
def exploreFurther(selected, visibility):
    relatives = pc.listRelatives(selected)
    
    for relative in relatives:
        if relative.type() == 'transform':
            exploreFurther(relative, visibility)
        elif relative.type() == 'mesh':
            print "Setting primary visibility of {0} to {1} ".format(relative, visibility)
            relative.setAttr('primaryVisibility', visibility)
            
def applyToSelected(*args):
    
    # Value queried from the checkbox
    checkboxValue = pc.checkBox(uiWidgets['visibility'], q=1, value=1)

    # Get the selected objects
    selections = pc.ls(sl=1)
    
    # If none, execution stops here
    if len(selections) == 0:
        pc.confirmDialog(t="Error", message="Nothing selected.", icon='critical')
    # Else, we batch set the primary visibility 
    else:
        print "BATCH SET VISIBILITY TO [%s]" % checkboxValue
        
        for sel in selections:
            exploreFurther(sel, checkboxValue)

def showUI():
    # Delete windows if already existing
    if pc.window("batchVisibility", exists=True):
        pc.deleteUI("batchVisibility")
    
    # Main window
    uiWidgets['window'] = pc.window("batchVisibility", menuBar=True, title="Batch set visibility", sizeable=False, h=430, w=300)
    
    uiWidgets['layout'] = pc.columnLayout()
    
    uiWidgets['visibility'] = pc.checkBox(label='Primary visibility', value=1)
    
    pc.button(l='Apply to selected', c=applyToSelected)
    
    pc.showWindow(uiWidgets['window'])
    
showUI()

