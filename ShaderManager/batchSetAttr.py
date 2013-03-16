import pymel.core as pc

# Dictionnary that contains all UI elements
uiWidgets = {}

# Explore recursively
def exploreFurther(selected, visibility, reflect, refract):
    relatives = pc.listRelatives(selected)
    
    for relative in relatives:
        if len(pc.listRelatives(relative)) != 0:
            exploreFurther(relative, visibility, reflect, refract)
        elif relative.type() == 'mesh':
            print "Setting primary visibility of {0} to {1} ".format(relative, visibility)
            relative.setAttr('primaryVisibility', visibility)
            print "Setting visible in Reflections of {0} to {1} ".format(relative, reflect)
            relative.setAttr('visibleInReflections', reflect)
            print "Setting visible in Refractions of {0} to {1} ".format(relative, refract)
            relative.setAttr('visibleInRefractions', refract)
            
def applyToSelected(*args):
    
    # Value queried from the checkbox
    visibilityValue = pc.checkBox(uiWidgets['visibility'], q=1, value=1)
    reflectValue = pc.checkBox(uiWidgets['visibleReflect'], q=1, value=1)
    refractValue = pc.checkBox(uiWidgets['visibleRefract'], q=1, value=1)

    # Get the selected objects
    selections = pc.ls(sl=1)
    
    # If none, execution stops here
    if len(selections) == 0:
        pc.confirmDialog(t="Error", message="Nothing selected.", icon='critical')
    # Else, we batch set the primary visibility 
    else:
        print "Batch setting visibility to [%s]" % visibilityValue
        print "Batch setting visible in Reflections to [%s]" % reflectValue
        print "Batch setting visible in Refractions to [%s]" % refractValue
        
        for sel in selections:
            exploreFurther(sel, visibilityValue, reflectValue, refractValue)

def showUI():
    # Delete windows if already existing
    if pc.window("batchVisibility", exists=True):
        pc.deleteUI("batchVisibility")
    
    # Main window
    uiWidgets['window'] = pc.window("batchVisibility", menuBar=True, title="Batch set visibility", sizeable=False, h=430, w=300)
    
    uiWidgets['layout'] = pc.columnLayout()
    
    uiWidgets['visibility'] = pc.checkBox(label='Primary visibility', value=1)
    uiWidgets['visibleReflect'] = pc.checkBox(label='Visible in Reflections', value=1)
    uiWidgets['visibleRefract'] = pc.checkBox(label='Visible in Refractions', value=1)
    
    pc.button(l='Apply to selected', c=applyToSelected)
    
    pc.showWindow(uiWidgets['window'])
    
showUI()

